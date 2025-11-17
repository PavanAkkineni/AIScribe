# AIscribe - Usage Examples

This document provides practical examples of using AIscribe with sample conversations and expected outputs.

## Example 1: Simple Fever Case

### Input Conversation

```
Doctor: Good morning! How are you feeling today?
Patient: Hi doctor, I'm not feeling well. I have a high fever.
Doctor: How long have you had the fever?
Patient: About three days now.
Doctor: What's your temperature been?
Patient: Around 102 to 103 degrees.
Doctor: Any other symptoms?
Patient: Yes, body aches and a runny nose.
Doctor: Based on your symptoms, you have a severe fever with mild cold symptoms. 
        I'll prescribe Doro 150, Cyprosine, Indolo-160, and Citrogen.
Patient: Thank you, doctor.
Doctor: Please see another physician if symptoms persist after three days.
```

### Expected Output - Clinical Summary

**Chief Complaint:**
```
Fever
```

**History of Present Illness:**
```
The patient presents with a three-day history of high fever ranging from 102-103°F, 
accompanied by body aches and rhinorrhea. The patient reports feeling generally unwell. 
Clinical assessment indicates severe fever with mild cold-like symptoms.
```

**Assessment/Plan:**
```
- Fever, severe, with mild cold symptoms
- Medications prescribed:
  • Doro 150
  • Cyprosine
  • Indolo-160
  • Citrogen
- Advise patient to seek additional medical evaluation if symptoms persist beyond 
  three days or worsen
- Follow-up recommended as needed
```

### Expected Output - Medical Decision Making

```
Step 1: ICD-10-CM Coding
- R50.9: Fever, unspecified
  Justification: Patient presents with fever without specified underlying cause.

Step 2: CPT Coding
- 99212: Office visit for established patient, straightforward MDM
  Justification: Problem-focused history, straightforward medical decision-making.

Step 3: Medical Decision-Making (MDM)
1. Number of diagnoses or management options: Low
   Justification: Single diagnosis of unspecified fever
2. Amount and/or complexity of data: Minimal
   Justification: No laboratory tests or imaging ordered
3. Risk of complications: Low
   Justification: Standard fever management with OTC medications

Overall MDM Level: Straightforward
Justification: Single diagnosis, minimal data, low risk

Final Step: Consistency Check
ICD-10-CM (R50.9), CPT (99212), and MDM (Straightforward) are consistent.
```

---

## Example 2: Respiratory Issue

### Input Conversation

```
Doctor: What brings you in today?
Patient: I've been having trouble breathing and a persistent cough.
Doctor: How long has this been going on?
Patient: About a week now.
Doctor: Is the cough dry or producing mucus?
Patient: It's producing yellow mucus.
Doctor: Any fever or chest pain?
Patient: A low-grade fever, around 100 degrees, and some chest tightness.
Doctor: Let me listen to your lungs. I hear some wheezing. 
        This could be bronchitis.
Patient: What should I do?
Doctor: I'll prescribe an antibiotic and an inhaler. Get rest and drink plenty of fluids.
Patient: Okay, thank you.
```

### Expected Output - Clinical Summary

**Chief Complaint:**
```
Difficulty breathing and persistent productive cough
```

**History of Present Illness:**
```
Patient presents with a one-week history of respiratory symptoms including difficulty 
breathing and productive cough with yellow sputum. Associated symptoms include 
low-grade fever (100°F) and chest tightness. Physical examination reveals wheezing 
on lung auscultation, suggestive of bronchitis.
```

**Assessment/Plan:**
```
- Acute bronchitis, likely bacterial given productive cough with colored sputum
- Medications prescribed:
  • Antibiotic (unspecified)
  • Inhaler for bronchodilation
- Recommendations:
  • Adequate rest
  • Increased fluid intake
  • Monitor symptoms
- Follow-up if symptoms worsen or do not improve in 3-5 days
```

---

## Example 3: Complex Multi-System Case

### Input Conversation

```
Doctor: Tell me what's been bothering you.
Patient: I've been having headaches, dizziness, and my blood pressure has been high.
Doctor: When did these symptoms start?
Patient: The headaches started two weeks ago, dizziness about a week ago.
Doctor: Have you been taking your blood pressure medication?
Patient: Yes, but I sometimes forget.
Doctor: What are your current medications?
Patient: Lisinopril 10mg daily.
Doctor: Let me check your blood pressure. It's 160/95, which is quite high.
Patient: Is that dangerous?
Doctor: It can be if not controlled. I'm going to increase your Lisinopril to 20mg 
        and add Hydrochlorothiazide.
Patient: Should I be worried about the headaches?
Doctor: The headaches are likely related to the high blood pressure. 
        Once we get it under control, they should improve.
Patient: Okay, what else should I do?
Doctor: Monitor your blood pressure at home, reduce salt intake, 
        and come back in two weeks for a follow-up.
Patient: I will. Thank you.
```

### Expected Output - Clinical Summary

**Chief Complaint:**
```
Headaches, dizziness, and elevated blood pressure
```

**History of Present Illness:**
```
Patient presents with a two-week history of headaches and one-week history of dizziness. 
Patient has a known history of hypertension and reports inconsistent adherence to 
prescribed Lisinopril 10mg daily. Current blood pressure reading is 160/95 mmHg, 
indicating poorly controlled hypertension. Patient attributes headaches to possible 
blood pressure elevation. No other neurological symptoms reported.
```

**Assessment/Plan:**
```
- Uncontrolled hypertension (BP 160/95 mmHg)
- Headache, likely secondary to hypertension
- Medication non-adherence

Management Plan:
- Increase Lisinopril from 10mg to 20mg daily
- Add Hydrochlorothiazide (dose not specified)
- Lifestyle modifications:
  • Home blood pressure monitoring
  • Sodium restriction
- Follow-up appointment in 2 weeks
- Patient education on medication adherence
- Monitor for improvement in headaches with blood pressure control
```

### Expected Output - Medical Decision Making

```
Step 1: ICD-10-CM Coding
- I10: Essential (primary) hypertension
  Justification: Patient has diagnosed hypertension with elevated BP reading
- R51.9: Headache, unspecified
  Justification: Patient reports headaches, likely secondary to hypertension
- R42: Dizziness and giddiness
  Justification: Patient reports dizziness symptoms
- Z91.19: Patient's noncompliance with other medical treatment and regimen
  Justification: Patient admits to inconsistent medication adherence

Step 2: CPT Coding
- 99213: Office visit, established patient, low complexity MDM
  Justification: Expanded history, medication adjustment, requires follow-up

Step 3: Medical Decision-Making (MDM)
1. Number of diagnoses or management options: Moderate
   Justification: Multiple diagnoses (hypertension, headache, dizziness, 
                  non-compliance) requiring medication adjustments
2. Amount and/or complexity of data: Limited
   Justification: Blood pressure measurement performed, medication review conducted
3. Risk of complications: Moderate
   Justification: Uncontrolled hypertension poses risk of cardiovascular events; 
                  medication changes require monitoring

Overall MDM Level: Low Complexity
Justification: Multiple problems, limited data reviewed, moderate risk requires 
               careful management and follow-up

Final Step: Consistency Check
ICD-10-CM codes (I10, R51.9, R42, Z91.19), CPT code (99213), and MDM level 
(Low Complexity) are consistent with the clinical documentation.
```

---

## Usage Tips

### For Best Results

1. **Clear Audio Quality**
   - Use a quiet environment
   - Speak clearly and at a moderate pace
   - Position microphone appropriately

2. **Complete Conversations**
   - Include opening greetings
   - State chief complaint clearly
   - Discuss symptoms in detail
   - Include treatment plan
   - Mention follow-up instructions

3. **Medical Terminology**
   - Use proper medical terms when possible
   - Spell out medication names clearly
   - Include dosages when prescribing
   - Mention vital signs if taken

4. **Speaker Distinction**
   - Ensure clear voice differences between doctor and patient
   - Avoid overlapping speech
   - Take turns speaking

### Common Issues and Solutions

**Issue**: Speakers not correctly identified
- **Solution**: Ensure distinct voices, avoid speaking over each other

**Issue**: Incomplete transcription
- **Solution**: Check audio quality, avoid background noise

**Issue**: Generic summaries
- **Solution**: Include more specific medical details in conversation

**Issue**: Incorrect coding
- **Solution**: Provide clear diagnosis and treatment information

---

## Testing the System

### Quick Test Script

Here's a simple conversation you can use to test the system:

```
Doctor: Hello, what brings you in today?
Patient: I've been feeling sick with a fever.
Doctor: How high is your fever?
Patient: About 101 degrees.
Doctor: Any other symptoms?
Patient: A sore throat and tiredness.
Doctor: Let me check you. Your throat is red. You likely have a viral infection.
        I'll prescribe some rest and fluids. Take ibuprofen for the fever.
Patient: Thank you, doctor.
Doctor: Come back if you're not better in a few days.
```

This should generate:
- ✓ Transcription with doctor/patient labels
- ✓ Chief Complaint: Fever
- ✓ Basic HPI and Assessment
- ✓ ICD-10 code for fever
- ✓ CPT code for office visit

---

## Advanced Examples

### Example 4: Follow-up Visit

```
Doctor: Welcome back. How have you been since your last visit?
Patient: Much better! The antibiotics really helped.
Doctor: Good to hear. Any remaining symptoms?
Patient: No, the cough is completely gone.
Doctor: Let me listen to your lungs. They sound clear now.
Patient: So I'm all better?
Doctor: Yes, you can stop the medication. Call if symptoms return.
```

Expected: Lower complexity coding due to follow-up nature.

### Example 5: Referral Case

```
Doctor: I've reviewed your test results.
Patient: What did they show?
Doctor: Your cholesterol is very high. I'd like you to see a cardiologist.
Patient: Is it serious?
Doctor: It needs management to prevent heart problems. I'm referring you to 
        Dr. Smith at the Heart Center.
Patient: Should I start any medication now?
Doctor: I'll prescribe a statin, but the cardiologist will adjust as needed.
```

Expected: Referral documentation and coordination of care codes.

---

## Notes

- All examples are fictional and for demonstration purposes only
- Actual AI output may vary slightly based on model performance
- The system learns to recognize medical patterns from the conversation structure
- More detailed conversations produce more accurate coding



