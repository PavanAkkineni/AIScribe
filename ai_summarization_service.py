"""AI Summarization service using OpenRouter API with fallback models"""

import requests
import json
from openai import OpenAI
from logger_config import setup_logger
from config import OPENROUTER_API_KEY, OPENROUTER_API_KEY_BACKUP, PRIMARY_MODEL, FALLBACK_MODEL, OPENROUTER_BASE_URL

logger = setup_logger()

class AISummarizationService:
    """Generate medical summaries using OpenRouter API with multiple models and backup keys"""
    
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.api_key_backup = OPENROUTER_API_KEY_BACKUP
        self.base_url = OPENROUTER_BASE_URL
        self.primary_model = PRIMARY_MODEL
        self.fallback_model = FALLBACK_MODEL
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        self.client_backup = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key_backup
        )
        logger.info("✓ AISummarizationService initialized with OpenRouter and backup key")
    
    def generate_clinical_summary(self, conversation_text):
        """
        Generate clinical summary with Chief Complaint, History, and Assessment/Plan
        
        Args:
            conversation_text: The doctor-patient conversation
            
        Returns:
            dict: Contains the clinical summary sections
        """
        logger.info("🏥 Generating clinical summary...")
        
        prompt = f"""You are a medical documentation assistant. Based on the following doctor-patient conversation, create a comprehensive medical note with the following sections:

1. **Chief Complaint**: Brief statement of the main reason for visit (1-2 sentences)
2. **History of Present Illness**: Detailed description of symptoms, severity, duration, and clinical observations
3. **Assessment/Plan**: Diagnosis, medications prescribed, and recommendations

Conversation:
{conversation_text}

Format your response EXACTLY as follows:

CHIEF_COMPLAINT:
[content here]

HISTORY_OF_PRESENT_ILLNESS:
[content here]

ASSESSMENT_PLAN:
[content here]

Be concise, professional, and include all relevant medical details mentioned in the conversation."""

        result = self._call_ai_with_fallback(prompt, "Clinical Summary")
        
        if result['success']:
            # Parse the response into sections
            parsed = self._parse_clinical_summary(result['response'])
            parsed['model_used'] = result['model_used']
            return parsed
        
        return result
    
    def generate_medical_decision_making(self, conversation_text, clinical_summary):
        """
        Generate Medical Decision Making summary with ICD-10 and CPT coding
        
        Args:
            conversation_text: The doctor-patient conversation
            clinical_summary: Previously generated clinical summary
            
        Returns:
            dict: Contains MDM analysis with coding
        """
        logger.info("📊 Generating Medical Decision Making summary...")
        
        prompt = f"""You are a medical coding and documentation specialist. Based on the following clinical information, provide a comprehensive Medical Decision Making (MDM) analysis.

CONVERSATION:
{conversation_text}

CLINICAL SUMMARY:
Chief Complaint: {clinical_summary.get('chief_complaint', 'N/A')}
History: {clinical_summary.get('history_of_present_illness', 'N/A')}
Assessment/Plan: {clinical_summary.get('assessment_plan', 'N/A')}

Provide a detailed MDM analysis with the following structure:

**Step 1: ICD-10-CM Coding**
- List relevant ICD-10-CM codes with descriptions
- Provide justification for each code

**Step 2: CPT Coding**
- List relevant CPT codes with descriptions
- Provide justification based on the visit complexity

**Step 3: Medical Decision-Making (MDM)**
1. **Number of diagnoses or management options**: [Low/Moderate/High]
   - Justification: [explain]
2. **Amount and/or complexity of data reviewed and analyzed**: [Minimal/Limited/Moderate/Extensive]
   - Justification: [explain]
3. **Risk of complications and/or morbidity or mortality of management**: [Low/Moderate/High]
   - Justification: [explain]

**Overall MDM Level**: [Straightforward/Low/Moderate/High]
- Justification: [explain]

**Final Step: Consistency Check**
- Verify that ICD-10-CM codes, CPT codes, and MDM level are consistent with documentation

Be specific, accurate, highlight headings and subheadings and follow medical coding guidelines."""

        result = self._call_ai_with_fallback(prompt, "Medical Decision Making")
        
        if result['success']:
            return {
                'success': True,
                'mdm_summary': result['response'],
                'model_used': result['model_used']
            }
        
        return result
    
    def _call_ai_with_fallback(self, prompt, summary_type):
        """
        Call AI model with automatic fallback (4 attempts total: 2 models × 2 API keys)
        
        Args:
            prompt: The prompt to send
            summary_type: Type of summary being generated (for logging)
            
        Returns:
            dict: Contains response and metadata
        """
        # Attempt 1: Primary API key + Primary model (Llama)
        logger.info(f"🤖 Attempt 1/4: {summary_type} with primary API key + {self.primary_model}")
        result = self._call_openrouter(prompt, self.primary_model, self.client, "Primary API")
        
        if result['success']:
            logger.info(f"✓ {summary_type} generated successfully (Attempt 1/4)")
            return result
        
        # Attempt 2: Primary API key + Fallback model (DeepSeek)
        logger.warning(f"⚠️ Attempt 1 failed: {result.get('error', 'Unknown error')}")
        logger.info(f"🔄 Attempt 2/4: {summary_type} with primary API key + {self.fallback_model}")
        
        result = self._call_openrouter(prompt, self.fallback_model, self.client, "Primary API")
        
        if result['success']:
            logger.info(f"✓ {summary_type} generated successfully (Attempt 2/4)")
            return result
        
        # Attempt 3: Backup API key + Primary model (Llama)
        logger.warning(f"⚠️ Attempt 2 failed: {result.get('error', 'Unknown error')}")
        logger.info(f"🔄 Attempt 3/4: {summary_type} with backup API key + {self.primary_model}")
        
        result = self._call_openrouter(prompt, self.primary_model, self.client_backup, "Backup API")
        
        if result['success']:
            logger.info(f"✓ {summary_type} generated successfully (Attempt 3/4)")
            return result
        
        # Attempt 4: Backup API key + Fallback model (DeepSeek)
        logger.warning(f"⚠️ Attempt 3 failed: {result.get('error', 'Unknown error')}")
        logger.info(f"🔄 Attempt 4/4: {summary_type} with backup API key + {self.fallback_model}")
        
        result = self._call_openrouter(prompt, self.fallback_model, self.client_backup, "Backup API")
        
        if result['success']:
            logger.info(f"✓ {summary_type} generated successfully (Attempt 4/4)")
        else:
            logger.error(f"❌ All 4 attempts failed for {summary_type}")
        
        return result
    
    def _call_openrouter(self, prompt, model, client, api_key_type="Primary API", max_tokens=None):
        """
        Make API call to OpenRouter
        
        Args:
            prompt: The prompt to send
            model: Model identifier
            client: OpenAI client instance to use
            api_key_type: Type of API key being used (for logging)
            max_tokens: Optional maximum tokens for response
            
        Returns:
            dict: Response data
        """
        try:
            # Build request parameters
            request_params = {
                "extra_headers": {
                    "HTTP-Referer": "https://aiscribe.local",
                    "X-Title": "AIscribe Medical Transcription",
                },
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert medical documentation assistant specializing in clinical notes and medical coding."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,  # Lower temperature for more consistent medical documentation
            }
            
            # Add max_tokens if specified
            if max_tokens:
                request_params["max_tokens"] = max_tokens
            
            completion = client.chat.completions.create(**request_params)
            
            response_text = completion.choices[0].message.content
            
            return {
                'success': True,
                'response': response_text,
                'model_used': f"{model} ({api_key_type})"
            }
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ API call failed for {model} with {api_key_type}: {error_msg}")
            
            return {
                'success': False,
                'error': error_msg,
                'model_used': f"{model} ({api_key_type})"
            }
    
    def _parse_clinical_summary(self, response_text):
        """
        Parse the clinical summary response into structured sections
        
        Args:
            response_text: Raw AI response
            
        Returns:
            dict: Parsed sections
        """
        sections = {
            'success': True,
            'chief_complaint': '',
            'history_of_present_illness': '',
            'assessment_plan': ''
        }
        
        try:
            # Split by section headers
            text = response_text.strip()
            
            # Extract Chief Complaint
            if 'CHIEF_COMPLAINT:' in text:
                start = text.find('CHIEF_COMPLAINT:') + len('CHIEF_COMPLAINT:')
                end = text.find('HISTORY_OF_PRESENT_ILLNESS:')
                sections['chief_complaint'] = text[start:end].strip()
            
            # Extract History of Present Illness
            if 'HISTORY_OF_PRESENT_ILLNESS:' in text:
                start = text.find('HISTORY_OF_PRESENT_ILLNESS:') + len('HISTORY_OF_PRESENT_ILLNESS:')
                end = text.find('ASSESSMENT_PLAN:')
                sections['history_of_present_illness'] = text[start:end].strip()
            
            # Extract Assessment/Plan
            if 'ASSESSMENT_PLAN:' in text:
                start = text.find('ASSESSMENT_PLAN:') + len('ASSESSMENT_PLAN:')
                sections['assessment_plan'] = text[start:].strip()
            
            logger.info("✓ Clinical summary parsed successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Error parsing clinical summary: {str(e)}")
            # Fallback: return the whole response
            sections['chief_complaint'] = response_text
        
        return sections

