"""Main Flask application for AIscribe"""

from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import json
from functools import wraps

from logger_config import setup_logger
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_FILE_SIZE, PRIMARY_MODEL, FALLBACK_MODEL, OPENAI_API_KEY
from transcription_service import TranscriptionService
from ai_summarization_service import AISummarizationService
from auth_service import AuthService
from email_service import EmailService
from openai import OpenAI
import base64

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production-12345'  # Change in production!

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize services
logger = setup_logger()
transcription_service = TranscriptionService()
ai_service = AISummarizationService()
auth_service = AuthService()
email_service = EmailService()
openai_client = OpenAI(api_key=OPENAI_API_KEY)  # For vision tasks

logger.info("=" * 80)
logger.info("🚀 AIscribe Application Starting")
logger.info("=" * 80)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@login_required
def index():
    """Serve the recordings dashboard"""
    user = auth_service.get_user(session['user_email'])
    return render_template('dashboard.html', user=user)

@app.route('/record/<patient_id>')
@login_required
def record(patient_id):
    """Serve the recording interface with patient ID"""
    user = auth_service.get_user(session['user_email'])
    return render_template('record_interface.html', user=user, patient_id=patient_id)

@app.route('/recording/<path:recording_id>')
@login_required
def view_recording(recording_id):
    """View a specific recording"""
    try:
        # recording_id is in format: patient_id/timestamp
        # Load recording data from patient_id/timestamp_results.json
        parts = recording_id.split('/')
        patient_id = parts[0]
        timestamp = parts[1] if len(parts) > 1 else ''
        
        results_file = os.path.join(app.config['UPLOAD_FOLDER'], patient_id, f"{timestamp}_results.json")
        
        if not os.path.exists(results_file):
            return "Recording not found", 404
        
        with open(results_file, 'r', encoding='utf-8') as f:
            recording_data = json.load(f)
        
        # Format the data for display
        recording = {
            'id': recording_id,
            'title': recording_data.get('patient_id', 'Untitled'),
            'date': datetime.fromisoformat(recording_data['timestamp']).strftime('%m/%d/%Y, %I:%M %p'),
            'duration': f"{int(recording_data.get('transcription', {}).get('duration', 0) // 60)} mins",
            'conversation_text': recording_data.get('conversation_text', 'N/A'),
            'clinical_summary': recording_data.get('clinical_summary', {}),
            'mdm_summary': recording_data.get('mdm_summary', {}).get('mdm_summary', 'N/A')
        }
        
        return render_template('recording_detail.html', recording=recording)
    except Exception as e:
        logger.error(f"Error loading recording: {str(e)}")
        return f"Error loading recording: {str(e)}", 500

@app.route('/signup')
def signup():
    """Serve the signup page"""
    if 'user_email' in session:
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/login')
def login():
    """Serve the login page"""
    if 'user_email' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('user_email', None)
    return redirect(url_for('login'))

@app.route('/pricing')
def pricing():
    """Pricing page placeholder"""
    return jsonify({'message': 'Pricing page coming soon'})

@app.route('/api/signup', methods=['POST'])
def api_signup():
    """Handle user signup"""
    try:
        data = request.get_json()
        
        result = auth_service.signup(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=data.get('password'),
            newsletter=data.get('newsletter', False)
        )
        
        if result['success']:
            # Auto-login after signup
            session['user_email'] = data.get('email')
            logger.info(f"New user signed up: {data.get('email')}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Signup failed. Please try again.'
        }), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    """Handle user login"""
    try:
        data = request.get_json()
        
        result = auth_service.login(
            email=data.get('email'),
            password=data.get('password')
        )
        
        if result['success']:
            session['user_email'] = data.get('email')
            logger.info(f"User logged in: {data.get('email')}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Login failed. Please try again.'
        }), 500

@app.route('/api/recordings', methods=['GET'])
@login_required
def get_recordings():
    """Get list of all recordings organized by patient"""
    try:
        recordings = []
        upload_folder = app.config['UPLOAD_FOLDER']
        
        # Iterate through patient folders
        if os.path.exists(upload_folder):
            for patient_id in os.listdir(upload_folder):
                patient_path = os.path.join(upload_folder, patient_id)
                
                # Skip if not a directory
                if not os.path.isdir(patient_path):
                    continue
                
                # Look for all *_results.json files in patient folder
                for filename in os.listdir(patient_path):
                    if filename.endswith('_results.json'):
                        results_file = os.path.join(patient_path, filename)
                        
                        try:
                            with open(results_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            
                            # Extract timestamp from filename (YYYYMMDD_HHMMSS_results.json)
                            timestamp_from_file = filename.replace('_results.json', '')
                            
                            # Format timestamp
                            timestamp_str = data.get('timestamp', '')
                            try:
                                dt = datetime.fromisoformat(timestamp_str)
                                date_formatted = dt.strftime('%B %d')  # e.g., "November 14"
                                time_formatted = dt.strftime('%m/%d/%Y, %I:%M %p')
                            except:
                                date_formatted = 'Unknown Date'
                                time_formatted = 'N/A'
                            
                            # Create recording ID from patient and timestamp
                            recording_id = f"{patient_id}/{timestamp_from_file}"
                            
                            recordings.append({
                                'id': recording_id,
                                'title': data.get('filename', patient_id).split('.')[0],
                                'patient_id': patient_id,
                                'timestamp': time_formatted,
                                'date': date_formatted,
                                'created_at': timestamp_str
                            })
                        except Exception as e:
                            logger.warning(f"Error loading recording {results_file}: {str(e)}")
                            continue
        
        # Sort by newest first
        recordings.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'success': True,
            'recordings': recordings
        })
    except Exception as e:
        logger.error(f"Error getting recordings: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recording/<path:recording_id>', methods=['DELETE'])
@login_required
def delete_recording(recording_id):
    """Delete a specific recording"""
    try:
        # recording_id is in format: patient_id/timestamp
        parts = recording_id.split('/')
        patient_id = parts[0]
        timestamp = parts[1] if len(parts) > 1 else ''
        
        patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], patient_id)
        
        # Delete results file and audio file
        results_file = os.path.join(patient_folder, f"{timestamp}_results.json")
        audio_files = [f for f in os.listdir(patient_folder) if f.startswith(timestamp) and not f.endswith('_results.json')]
        
        deleted = False
        
        if os.path.exists(results_file):
            os.remove(results_file)
            deleted = True
            logger.info(f"Deleted results file: {results_file}")
        
        for audio_file in audio_files:
            audio_path = os.path.join(patient_folder, audio_file)
            if os.path.exists(audio_path):
                os.remove(audio_path)
                deleted = True
                logger.info(f"Deleted audio file: {audio_path}")
        
        if deleted:
            return jsonify({
                'success': True,
                'message': 'Recording deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Recording not found'
            }), 404
            
    except Exception as e:
        logger.error(f"Error deleting recording: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/process-audio', methods=['POST'])
@login_required
def process_audio():
    """
    Main endpoint to process audio file:
    1. Transcribe with speaker diarization
    2. Generate clinical summary
    3. Generate MDM summary
    """
    logger.info("\n" + "=" * 80)
    logger.info("📥 New audio processing request received")
    logger.info("=" * 80)
    
    try:
        # Check if file is present
        if 'audio' not in request.files:
            logger.error("❌ No audio file provided in request")
            return jsonify({
                'success': False,
                'error': 'No audio file provided'
            }), 400
        
        file = request.files['audio']
        patient_id = request.form.get('patient_id', 'unknown_patient')
        patient_email = request.form.get('patient_email', '')
        recording_type = request.form.get('recording_type', 'conversation')  # 'conversation' or 'summary'
        
        logger.info(f"📝 Recording type: {recording_type}")
        
        if file.filename == '':
            logger.error("❌ Empty filename")
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            logger.error(f"❌ Invalid file type: {file.filename}")
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Create patient folder structure (one folder per patient)
        patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(patient_id))
        os.makedirs(patient_folder, exist_ok=True)
        
        # Save the uploaded file directly in patient folder with timestamp
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_with_timestamp = f"{timestamp}_{filename}"
        filepath = os.path.join(patient_folder, filename_with_timestamp)
        
        logger.info(f"💾 Saving file to: {patient_folder}/{filename_with_timestamp}")
        file.save(filepath)
        logger.info(f"✓ File saved successfully")
        
        # Step 1: Transcribe audio (with or without speaker diarization based on recording type)
        enable_diarization = (recording_type == 'conversation')
        
        logger.info("\n" + "-" * 80)
        if enable_diarization:
            logger.info("STEP 1: TRANSCRIPTION WITH SPEAKER DIARIZATION")
        else:
            logger.info("STEP 1: TRANSCRIPTION (SUMMARY NOTES MODE)")
        logger.info("-" * 80)
        
        transcription_result = transcription_service.transcribe_audio(filepath, enable_diarization=enable_diarization)
        
        if not transcription_result['success']:
            logger.error(f"❌ Transcription failed: {transcription_result.get('error')}")
            return jsonify(transcription_result), 500
        
        dialogue = transcription_result['dialogue']
        conversation_text = transcription_service.format_dialogue_text(dialogue)
        
        logger.info(f"✓ Transcription completed: {len(conversation_text)} characters")
        
        # Step 2: Generate clinical summary
        logger.info("\n" + "-" * 80)
        logger.info("STEP 2: GENERATING CLINICAL SUMMARY")
        logger.info("-" * 80)
        
        clinical_summary = ai_service.generate_clinical_summary(conversation_text)
        
        if not clinical_summary['success']:
            logger.error(f"❌ Clinical summary generation failed")
            return jsonify({
                'success': False,
                'error': 'Failed to generate clinical summary',
                'transcription': transcription_result
            }), 500
        
        logger.info(f"✓ Clinical summary generated using: {clinical_summary['model_used']}")
        
        # Step 3: Generate Medical Decision Making summary
        logger.info("\n" + "-" * 80)
        logger.info("STEP 3: GENERATING MEDICAL DECISION MAKING SUMMARY")
        logger.info("-" * 80)
        
        mdm_summary = ai_service.generate_medical_decision_making(
            conversation_text,
            clinical_summary
        )
        
        if not mdm_summary['success']:
            logger.error(f"❌ MDM summary generation failed")
            # Still return clinical summary even if MDM fails
            return jsonify({
                'success': True,
                'transcription': transcription_result,
                'conversation_text': conversation_text,
                'clinical_summary': clinical_summary,
                'mdm_summary': {'success': False, 'error': 'MDM generation failed'},
                'warning': 'MDM summary could not be generated'
            }), 200
        
        logger.info(f"✓ MDM summary generated using: {mdm_summary['model_used']}")
        
        # Generate and send patient email
        logger.info("\n" + "-" * 80)
        logger.info("STEP 4: GENERATING AND SENDING PATIENT EMAIL")
        logger.info("-" * 80)
        
        generated_email = generate_patient_email(clinical_summary, mdm_summary)
        logger.info("✓ Patient email generated")
        
        # Prepare email data
        email_data = {
            'timestamp': datetime.now().isoformat(),
            'patient_id': patient_id,
            'to': patient_email if patient_email else f"{patient_id}@patient.email",
            'subject': generated_email['subject'],
            'body': generated_email['body'],
            'direction': 'outbound',
            'sent': False
        }
        
        # Actually send email if patient email is provided
        if patient_email and patient_email.strip():
            logger.info(f"📤 Sending email to: {patient_email}")
            send_result = email_service.send_email(
                to_email=patient_email,
                subject=generated_email['subject'],
                body_html=generated_email['body'],
                patient_id=patient_id
            )
            
            if send_result['success']:
                email_data['sent'] = True
                email_data['sent_at'] = send_result.get('sent_at')
                logger.info(f"✅ Email sent successfully to {patient_email}")
            else:
                email_data['send_error'] = send_result.get('error')
                logger.warning(f"⚠️ Email sending failed: {send_result.get('error')}")
        else:
            logger.info("ℹ️ No patient email provided, email not sent")
        
        # Save email to patient folder
        email_filename = f"{timestamp}_email.json"
        email_filepath = os.path.join(patient_folder, email_filename)
        
        with open(email_filepath, 'w', encoding='utf-8') as f:
            json.dump(email_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Email saved to: {patient_folder}/{email_filename}")
        
        # Save results to a JSON file in the patient folder with timestamp
        results = {
            'timestamp': datetime.now().isoformat(),
            'filename': filename,
            'patient_id': patient_id,
            'recording_type': recording_type,
            'transcription': transcription_result,
            'conversation_text': conversation_text,
            'clinical_summary': clinical_summary,
            'mdm_summary': mdm_summary
        }
        
        results_filename = f"{timestamp}_results.json"
        results_filepath = os.path.join(patient_folder, results_filename)
        
        with open(results_filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Results saved to: {patient_folder}/{results_filename}")
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ PROCESSING COMPLETED SUCCESSFULLY")
        logger.info("=" * 80 + "\n")
        
        return jsonify({
            'success': True,
            'transcription': transcription_result,
            'conversation_text': conversation_text,
            'clinical_summary': clinical_summary,
            'mdm_summary': mdm_summary,
            'patient_id': patient_id,
            'recording_id': f"{patient_id}/{timestamp}"
        })
    
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        logger.exception(e)
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/results/<filename>')
@login_required
def get_results(filename):
    """Retrieve saved results"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logger.error(f"❌ Error retrieving results: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Results not found'
        }), 404

@app.route('/api/patient/<patient_id>/emails', methods=['GET'])
@login_required
def get_patient_emails(patient_id):
    """Get all emails for a specific patient (sent emails from local storage)"""
    try:
        patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(patient_id))
        
        if not os.path.exists(patient_folder):
            return jsonify({
                'success': True,
                'emails': []
            })
        
        emails = []
        
        # Find all email files for this patient
        for filename in os.listdir(patient_folder):
            if filename.endswith('_email.json'):
                email_path = os.path.join(patient_folder, filename)
                try:
                    with open(email_path, 'r', encoding='utf-8') as f:
                        email_data = json.load(f)
                        emails.append(email_data)
                except Exception as e:
                    logger.warning(f"Error loading email {filename}: {str(e)}")
                    continue
        
        # Sort by timestamp (newest first)
        emails.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return jsonify({
            'success': True,
            'emails': emails
        })
    except Exception as e:
        logger.error(f"Error getting emails for patient {patient_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/patient/<patient_id>/fetch-inbox', methods=['POST'])
@login_required
def fetch_patient_inbox(patient_id):
    """Fetch new emails from inbox for a specific patient"""
    try:
        logger.info(f"📬 Fetching inbox emails for patient: {patient_id}")
        
        # Get patient email from request or find it in existing emails
        patient_email = None
        if request.is_json and request.json:
            patient_email = request.json.get('patient_email')
        
        if not patient_email:
            # Try to find patient email from existing sent emails
            patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(patient_id))
            if os.path.exists(patient_folder):
                for filename in os.listdir(patient_folder):
                    if filename.endswith('_email.json') and not filename.startswith('inbox_'):
                        try:
                            with open(os.path.join(patient_folder, filename), 'r', encoding='utf-8') as f:
                                email_data = json.load(f)
                                if email_data.get('to') and '@' in email_data.get('to', ''):
                                    patient_email = email_data['to']
                                    break
                        except:
                            continue
        
        if not patient_email:
            return jsonify({
                'success': False,
                'error': 'Patient email not found. Please ensure an email was sent to this patient first.'
            }), 400
        
        logger.info(f"   Patient email: {patient_email}")
        
        # Fetch emails from IMAP using patient email
        inbox_emails = email_service.fetch_inbox_emails(patient_email=patient_email, limit=50)
        
        if not inbox_emails:
            return jsonify({
                'success': True,
                'new_emails': 0,
                'message': 'No new emails found'
            })
        
        # Save new emails to patient folder
        patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(patient_id))
        os.makedirs(patient_folder, exist_ok=True)
        
        new_count = 0
        for email_data in inbox_emails:
            # Add patient_id to email data
            email_data['patient_id'] = patient_id
            
            # Create filename from email ID
            email_id_hash = hash(email_data.get('id', ''))
            email_filename = f"inbox_{abs(email_id_hash)}_email.json"
            email_path = os.path.join(patient_folder, email_filename)
            
            # Skip if already exists
            if os.path.exists(email_path):
                continue
            
            # Save email
            with open(email_path, 'w', encoding='utf-8') as f:
                json.dump(email_data, f, indent=2, ensure_ascii=False)
            new_count += 1
        
        logger.info(f"✅ Saved {new_count} new emails for patient {patient_id}")
        
        return jsonify({
            'success': True,
            'new_emails': new_count,
            'total_fetched': len(inbox_emails),
            'message': f'Found {new_count} new email(s)'
        })
        
    except Exception as e:
        logger.error(f"Error fetching inbox for patient {patient_id}: {str(e)}")
        logger.exception(e)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/patient/<patient_id>/health-summary', methods=['POST'])
@login_required
def generate_patient_health_summary(patient_id):
    """Generate comprehensive patient health summary from all clinical records"""
    try:
        logger.info(f"📋 Generating health summary for patient: {patient_id}")
        
        patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(patient_id))
        
        if not os.path.exists(patient_folder):
            return jsonify({
                'success': False,
                'error': 'No records found for this patient'
            }), 404
        
        # Collect all clinical summaries from patient's recordings
        clinical_records = []
        
        for filename in os.listdir(patient_folder):
            if filename.endswith('_results.json'):
                results_path = os.path.join(patient_folder, filename)
                try:
                    with open(results_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        visit_date = data.get('timestamp', 'Unknown date')
                        clinical_summary = data.get('clinical_summary', {})
                        
                        if clinical_summary:
                            record = f"""
Visit Date: {visit_date}
Chief Complaint: {clinical_summary.get('chief_complaint', 'N/A')}
History of Present Illness: {clinical_summary.get('history_of_present_illness', 'N/A')}
Assessment and Plan: {clinical_summary.get('assessment_plan', 'N/A')}
---
"""
                            clinical_records.append(record)
                except Exception as e:
                    logger.warning(f"Error loading record {filename}: {str(e)}")
                    continue
        
        if not clinical_records:
            return jsonify({
                'success': False,
                'error': 'No clinical summaries found for this patient'
            }), 404
        
        # Combine all records
        all_records = '\n'.join(clinical_records)
        
        logger.info(f"   Found {len(clinical_records)} clinical record(s)")
        
        # Generate comprehensive summary using AI
        prompt = f"""You are a medical records specialist. Based on the following clinical records for patient {patient_id}, create a comprehensive health history summary.

CLINICAL RECORDS:
{all_records}

Please provide a detailed health summary including:
1. **Patient Overview**: Brief introduction
2. **Medical History Timeline**: Chronological summary of visits and conditions
3. **Recurring Conditions**: Any patterns or recurring health issues
4. **Current Health Status**: Latest assessment
5. **Treatment Summary**: Medications and interventions prescribed
6. **Follow-up Recommendations**: Any ongoing care needs

Be professional, concise, and focus on key medical information. Format with clear headers and bullet points."""
        
        # Use Llama model for summary generation
        try:
            result = ai_service._call_openrouter(
                prompt,
                model=PRIMARY_MODEL,
                client=ai_service.client,
                api_key_type="Primary API",
                max_tokens=800
            )
            
            if result['success']:
                summary_text = result['response']
                model_used = "Clinical AI"
            else:
                raise Exception(result.get('error', 'Unknown error'))
        except Exception as e:
            logger.warning(f"   Primary model failed, using fallback: {str(e)}")
            result = ai_service._call_openrouter(
                prompt,
                model=FALLBACK_MODEL,
                client=ai_service.client,
                api_key_type="Primary API",
                max_tokens=800
            )
            
            if result['success']:
                summary_text = result['response']
                model_used = "Clinical AI (Fallback)"
            else:
                raise Exception(result.get('error', 'Failed to generate summary'))
        
        logger.info(f"   ✅ Health summary generated successfully")
        
        return jsonify({
            'success': True,
            'summary': summary_text,
            'total_visits': len(clinical_records),
            'model_used': model_used
        })
        
    except Exception as e:
        logger.error(f"Error generating health summary: {str(e)}")
        logger.exception(e)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/patient/<patient_id>/send-reply', methods=['POST'])
@login_required
def send_patient_reply(patient_id):
    """Send a reply email to a patient"""
    try:
        data = request.get_json()
        patient_email = data.get('patient_email')
        subject = data.get('subject')
        body = data.get('body')
        reply_to_id = data.get('reply_to_id', '')
        
        if not patient_email or not subject or not body:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: patient_email, subject, body'
            }), 400
        
        logger.info(f"📤 Sending reply to patient {patient_id} ({patient_email})")
        
        # Send email
        send_result = email_service.send_email(
            to_email=patient_email,
            subject=subject,
            body_html=body,
            patient_id=patient_id
        )
        
        if not send_result['success']:
            return jsonify({
                'success': False,
                'error': f"Failed to send email: {send_result.get('error')}"
            }), 500
        
        # Save sent email to patient folder
        patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(patient_id))
        os.makedirs(patient_folder, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        email_data = {
            'timestamp': datetime.now().isoformat(),
            'patient_id': patient_id,
            'to': patient_email,
            'subject': subject,
            'body': body,
            'direction': 'outbound',
            'sent': True,
            'sent_at': send_result.get('sent_at'),
            'in_reply_to': reply_to_id
        }
        
        email_filename = f"{timestamp}_reply_email.json"
        email_path = os.path.join(patient_folder, email_filename)
        
        with open(email_path, 'w', encoding='utf-8') as f:
            json.dump(email_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Reply sent and saved")
        
        return jsonify({
            'success': True,
            'message': 'Reply sent successfully',
            'email': email_data
        })
        
    except Exception as e:
        logger.error(f"Error sending reply: {str(e)}")
        logger.exception(e)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/fetch-all-inbox', methods=['POST'])
@login_required
def fetch_all_inbox():
    """Fetch all new emails from inbox (for all patients)"""
    try:
        logger.info("📬 Fetching all inbox emails...")
        
        # Fetch all emails from IMAP
        inbox_emails = email_service.fetch_inbox_emails(limit=100)
        
        if not inbox_emails:
            return jsonify({
                'success': True,
                'new_emails': 0,
                'message': 'No new emails found'
            })
        
        # Group emails by patient and save
        total_saved = 0
        patients_updated = set()
        
        for email_data in inbox_emails:
            patient_id = email_data.get('patient_id', 'unknown')
            
            if patient_id == 'unknown':
                continue
            
            patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(patient_id))
            os.makedirs(patient_folder, exist_ok=True)
            
            # Create filename from email ID
            email_id_hash = hash(email_data.get('id', ''))
            email_filename = f"inbox_{abs(email_id_hash)}_email.json"
            email_path = os.path.join(patient_folder, email_filename)
            
            # Skip if already exists
            if os.path.exists(email_path):
                continue
            
            # Save email
            with open(email_path, 'w', encoding='utf-8') as f:
                json.dump(email_data, f, indent=2, ensure_ascii=False)
            
            total_saved += 1
            patients_updated.add(patient_id)
        
        logger.info(f"✅ Saved {total_saved} new emails for {len(patients_updated)} patients")
        
        return jsonify({
            'success': True,
            'new_emails': total_saved,
            'patients_updated': len(patients_updated),
            'message': f'Found {total_saved} new emails for {len(patients_updated)} patients'
        })
        
    except Exception as e:
        logger.error(f"Error fetching all inbox emails: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_patient_email(clinical_summary, mdm_summary):
    """Generate a patient email from clinical summary and MDM"""
    try:
        # Extract key information
        chief_complaint = clinical_summary.get('chief_complaint', 'N/A')
        assessment_plan = clinical_summary.get('assessment_and_plan', 'N/A')
        
        # Extract CPT codes and generate billing info
        cpt_codes = mdm_summary.get('mdm_summary', {}).get('cpt_coding', []) if isinstance(mdm_summary.get('mdm_summary'), dict) else []
        icd_codes = mdm_summary.get('mdm_summary', {}).get('icd10_cm_coding', []) if isinstance(mdm_summary.get('mdm_summary'), dict) else []
        
        # Build billing section
        billing_info = ""
        if cpt_codes:
            billing_info = "<h3>📋 Billing Information</h3>"
            billing_info += "<p><strong>CPT Codes:</strong></p><ul>"
            for code in cpt_codes:
                if isinstance(code, dict):
                    code_num = code.get('code', 'N/A')
                    description = code.get('description', 'N/A')
                    billing_info += f"<li>{code_num} - {description}</li>"
                else:
                    billing_info += f"<li>{code}</li>"
            billing_info += "</ul>"
        
        # Build email body
        email_body = f"""
<p>Dear Patient,</p>

<p>Thank you for your recent visit. Below is a summary of your consultation and next steps:</p>

<h3>📝 Visit Summary</h3>
<p><strong>Chief Complaint:</strong> {chief_complaint}</p>

<h3>🏥 Assessment and Treatment Plan</h3>
<p>{assessment_plan}</p>

<h3>💊 Medication Instructions</h3>
<p>Please follow the medication regimen as discussed during your visit. If you have any questions or concerns about your medications, don't hesitate to contact our office.</p>

{billing_info}

<h3>📞 Next Steps</h3>
<p>Please schedule a follow-up appointment as recommended. If you experience any worsening symptoms or have concerns, please contact our office immediately.</p>

<p><strong>Important:</strong> This is an automated summary. If you notice any discrepancies, please contact our office.</p>

<p>Best regards,<br>
AIscribe Medical Team</p>
        """.strip()
        
        return {
            'subject': f'Visit Summary - {chief_complaint[:50]}',
            'body': email_body
        }
    except Exception as e:
        logger.error(f"Error generating email: {str(e)}")
        return {
            'subject': 'Visit Summary',
            'body': '<p>Thank you for your visit. Please contact our office for your visit summary.</p>'
        }

@app.route('/api/chat-assistant', methods=['POST'])
@login_required
def chat_assistant():
    """AI Chat Assistant for platform, medical, and vision queries"""
    try:
        # Check if there's an image in the request
        has_image = 'image' in request.files
        
        if has_image:
            # Handle image + text query
            return handle_vision_query()
        else:
            # Handle text-only query
            return handle_text_query()
        
    except Exception as e:
        logger.error(f"❌ Chat Assistant Error: {str(e)}")
        logger.exception(e)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def handle_vision_query():
    """Handle queries with images using GPT-4o-mini"""
    try:
        image_file = request.files['image']
        user_message = request.form.get('message', 'What is in this image?').strip()
        
        logger.info(f"🖼️ Vision Query: {user_message[:100]}...")
        
        # Read and encode image to base64
        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Determine image mime type
        image_mime_type = image_file.content_type or 'image/jpeg'
        
        # System prompt for medical expert role
        system_prompt = """You are an experienced medical imaging specialist and clinical consultant providing a second opinion to practicing physicians. Your role is to offer detailed, evidence-based insights that help doctors in their diagnostic process.

Guidelines:
- Provide thorough, professional analysis of medical images
- Highlight key findings, abnormalities, or areas of concern
- Suggest differential diagnoses when appropriate
- Reference relevant clinical indicators and patterns
- Use precise medical terminology
- Note that your analysis is for consultation purposes, not definitive diagnosis
- critically analyze the image and specify medical issues like fractures or other injuries or other medical issues in the image.
Remember: Doctors will use your insights as a second opinion to inform their clinical judgment, not as a replacement for their professional decision-making."""
        
        # Call GPT-4o-mini with vision
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_message
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{image_mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=600
        )
        
        response_text = response.choices[0].message.content
        
        logger.info(f"   ✓ Vision response generated using GPT-4o-mini")
        
        return jsonify({
            'success': True,
            'response': response_text,
            'category': 'vision',
            'model_used': 'GPT-4o-mini (Vision AI)'
        })
        
    except Exception as e:
        logger.error(f"❌ Vision Query Error: {str(e)}")
        logger.exception(e)
        return jsonify({
            'success': False,
            'error': f'Vision analysis failed: {str(e)}'
        }), 500

def handle_text_query():
    """Handle text-only queries using Llama/DeepSeek"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        logger.info(f"💬 Chat Assistant Query: {user_message[:100]}...")
        
        # Step 1: Categorize the query
        category = categorize_query(user_message)
        logger.info(f"   Category: {category}")
        
        # Step 2: Prepare context based on category
        if category == 'platform':
            system_prompt = """You are AIscribe assistant. Help users with platform features.

Key Features:
- START button → Enter patient ID → Record/Upload audio
- Patient folders on dashboard (collapsible)
- Email icon for patient communication
- Search bar for finding patients
- Click recording to view transcript & summaries

Be concise and clear."""
        else:  # medical
            system_prompt = """You are a medical AI assistant. Provide accurate medical information.
Always remind users to consult healthcare professionals. Be concise and evidence-based."""
        
        # Step 3: Generate response using existing LLM service
        full_prompt = f"{system_prompt}\n\nQuestion: {user_message}\n\nAnswer:"
        
        # Try primary model (using FREE tier from config)
        try:
            result = ai_service._call_openrouter(
                full_prompt,
                model=PRIMARY_MODEL,  # Uses free tier from config
                client=ai_service.client,
                api_key_type="Primary API",
                max_tokens=400
            )
            if result['success']:
                response_text = result['response']
                model_used = PRIMARY_MODEL
            else:
                raise Exception(result.get('error', 'Unknown error'))
        except Exception as e:
            logger.warning(f"   Primary model failed, using fallback: {str(e)}")
            # Fallback to DeepSeek (FREE tier)
            result = ai_service._call_openrouter(
                full_prompt,
                model=FALLBACK_MODEL,  # Uses free tier from config
                client=ai_service.client,
                api_key_type="Primary API",
                max_tokens=400
            )
            if result['success']:
                response_text = result['response']
                model_used = FALLBACK_MODEL
            else:
                raise Exception(result.get('error', 'Unknown error'))
        
        logger.info(f"   ✓ Response generated using: {model_used}")
        
        # Customize display name for medical queries to show medical AI branding
        display_model_name = model_used
        if category == 'medical':
            # Show a medical-specific AI name for credibility
            display_model_name = "Clinical-AI (Medical Language Model)"
        elif category == 'platform':
            display_model_name = "AIscribe Assistant"
        
        return jsonify({
            'success': True,
            'response': response_text,
            'category': category,
            'model_used': display_model_name
        })
        
    except Exception as e:
        logger.error(f"❌ Text Query Error: {str(e)}")
        logger.exception(e)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def categorize_query(message):
    """Categorize user query as 'platform' or 'medical'"""
    message_lower = message.lower()
    
    # Platform keywords
    platform_keywords = [
        'how to', 'how do i', 'where is', 'where can i', 'how can i',
        'record', 'upload', 'recording', 'save', 'delete', 'email',
        'patient folder', 'search', 'login', 'sign up', 'account',
        'dashboard', 'interface', 'button', 'click', 'navigate',
        'feature', 'use', 'aiscribe', 'platform', 'system',
        'transcript', 'summary', 'export', 'download'
    ]
    
    # Medical keywords
    medical_keywords = [
        'symptom', 'disease', 'condition', 'diagnosis', 'treatment',
        'medication', 'drug', 'icd', 'cpt', 'medical', 'clinical',
        'patient', 'fever', 'infection', 'pain', 'doctor',
        'therapy', 'prescription', 'dosage', 'side effect',
        'anatomy', 'physiology', 'pathology', 'syndrome'
    ]
    
    # Count matches
    platform_score = sum(1 for keyword in platform_keywords if keyword in message_lower)
    medical_score = sum(1 for keyword in medical_keywords if keyword in message_lower)
    
    # If clear platform query
    if platform_score > medical_score:
        return 'platform'
    # If clear medical query or both equal (default to medical for safety)
    else:
        return 'medical'

def get_platform_context():
    """Provide context about AIscribe platform features"""
    return """
AIscribe is a medical transcription and communication platform with these key features:

1. RECORDING & TRANSCRIPTION:
   - Click "START" button on dashboard
   - Enter patient ID/name
   - Record audio using microphone OR upload audio file
   - System transcribes with speaker diarization (identifies Doctor vs Patient)
   - Generates clinical summary and MDM report with ICD-10/CPT codes

2. PATIENT MANAGEMENT:
   - Dashboard shows all patients as collapsible folders
   - One folder per patient containing all their recordings
   - Click folder to expand and see recordings
   - Search bar to find patients quickly

3. EMAIL COMMUNICATION:
   - Click email icon (📧) next to patient folder
   - View complete email thread with patient
   - "Refresh Inbox" button fetches new patient replies
   - Compose replies directly in the interface
   - Emails include visit summary, medications, and billing info

4. VIEWING RECORDINGS:
   - Click on any recording to see:
     * Full conversation transcript
     * Clinical summary (Chief Complaint, History, Assessment)
     * MDM summary with ICD-10 and CPT codes
   - Delete recordings using trash icon

5. NAVIGATION:
   - Top menu: Blog, Recordings, Templates, Account, Logout
   - Search bar for finding patients
   - Sort recordings by newest/oldest/name

6. AUTHENTICATION:
   - Login/Signup pages
   - Secure session management
   - Logout button in top right
"""

if __name__ == '__main__':
    logger.info("🌐 Starting Flask server on http://localhost:5000")
    logger.info("📝 Open your browser and navigate to http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

