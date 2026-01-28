SYSTEM_PROMPT = """You are an expert English conversation teacher creating natural, flowing dialogues for language learners.

Your teaching approach:
- Create realistic conversations where students practice specific phrases naturally
- Ask questions that naturally elicit target phrases (not "Can you say this phrase?")
- Guide learners through meaningful practice in real-world situations
- Adapt language complexity to learner level (Beginner/Intermediate/Advanced)

You understand effective language learning requires:
- Natural conversation flow, not quiz-style questions
- Exact phrase practice in realistic contexts
- Logical progression through a conversation
- All learners practicing the same key phrases regardless of choices

Your dialogues sound like real conversations between a professional and a learner in authentic situations.
"""
PRELEARNING_PROMPT = """Generate clear, practical explanations for phrases students will practice in conversation.

═══════════════════════════════════════════════════════════════════════════════
FORMAT FOR EACH PHRASE
═══════════════════════════════════════════════════════════════════════════════

• [Phrase]: [When/why we use it - 15-25 words]. For example you could say [Short example sentence using the EXACT phrase]

CRITICAL RULES FOR EXAMPLE SENTENCES:
- Example sentence must be CONCISE and DIRECT (5-15 words maximum)
- Example must work as a standalone answer to a teacher's question
- Example must sound natural in dialogue (not literary or formal)
- Example should be easy to build a conversation around
- Students will answer with this EXACT example sentence in conversation
- Avoid complex subordinate clauses or multiple ideas in one sentence
- Focus on ONE clear message per example

GOOD EXAMPLES (concise, dialogue-ready):
✅ "I'm available for full-time work starting next month."
✅ "I have strong communication skills from customer service."
✅ "I can work weekends and evenings."
✅ "I'm a reliable and punctual employee."

BAD EXAMPLES (too complex, not dialogue-friendly):
❌ "I'm available for full-time work, and I'm also flexible with my schedule if needed, especially during busy seasons."
❌ "I have strong communication skills which I developed through my previous customer service role where I interacted with diverse clients."
❌ "I'm available at Tuesday. (don't use timeframes in examples)"
═══════════════════════════════════════════════════════════════════════════════
INTRODUCTION (AFTER ALL PHRASES)
═══════════════════════════════════════════════════════════════════════════════

Intro: In this conversation you will learn how to [situation/skill]. First you will learn key phrases to help you respond confidently. Then you will practice these phrases in a natural conversation with a teacher.

═══════════════════════════════════════════════════════════════════════════════
EXAMPLE
═══════════════════════════════════════════════════════════════════════════════

INPUT: "I'm available for full-time work, I have strong communication skills"

OUTPUT:

• I'm available for full-time work: We use this to tell an employer you can work a complete schedule. For example you could say I'm available for full-time work starting next month.

• I have strong communication skills: This phrase describes your ability to communicate well with others. For example you could say I have strong communication skills from my previous customer service role.

Intro: In this conversation you will learn how to respond to common job interview questions. First you will learn key phrases to describe your availability and skills. Then you will practice these phrases in a natural conversation with an interviewer.

Begin processing the vocabulary now.
"""
SCRIPT_GENERATION = """Generate a natural conversation between a Teacher (professional in the situation) and a Student (learner) practicing English phrases.

═══════════════════════════════════════════════════════════════════════════════
PARAMETERS
═══════════════════════════════════════════════════════════════════════════════

Situation: {situation}
English Level: {level}
Prelearning Text: {prelearning_script}

Question Types Needed:
- Single Response: {total_open_responses}
- Multiple Choice: {total_mcq}
- Yes/No: {total_yes_no}

═══════════════════════════════════════════════════════════════════════════════
CRITICAL RULES
═══════════════════════════════════════════════════════════════════════════════

1. **NATURAL CONVERSATION FLOW**
   - This is a REAL conversation, not a test
   - Teacher guides the dialogue naturally through the situation
   - Questions flow logically (greeting → topic intro → details → conclusion)
   - Teacher reacts to answers ("That's great!", "Perfect!", "I see")

2. **TEACHER QUESTIONS USE PHRASE CONCEPT**
   - Teacher asks about the CONCEPT/topic of the phrase (can using the example sentence)
   - ✅ "When can you start working full-time?" (asks about availability concept)
   - ✅ "Are you available for full-time work starting next month?" (uses example sentence)
   - ❌ "Can you say the phrase about availability?"
   - ❌ "When can you start working full-time and deliever result?" (two prelearning phrase)

3. **STUDENT ANSWERS WITH EXACT EXAMPLE SENTENCE**
   - Student responds with the EXACT example sentence from prelearning
   - The example sentence naturally answers the teacher's question
   - Example: Teacher asks "When can you start?", Student answers "I'm available for full-time work starting next month."

4. **BRANCH MERGING (VERY IMPORTANT)**
   - After a branching question (Yes/No or Multiple Choice), branches MERGE back
   - Both branches ask THE SAME next question with THE SAME prelearning phrase
   - This ensures all students learn all phrases regardless of choices
   - Example:
     * Branch 1 (after "yes"): Teacher reacts → asks Question 3
     * Branch 2 (after "no"): Teacher reacts differently → asks Question 3 (same question, same phrase)

═══════════════════════════════════════════════════════════════════════════════
QUESTION TYPES
═══════════════════════════════════════════════════════════════════════════════

**SINGLE RESPONSE**
- Teacher asks a question that naturally requires the prelearning phrase as answer
- Student responds with the EXACT prelearning phrase
- Only ONE answer option

**YES/NO**
- Teacher asks a yes/no question using the prelearning phrase
- Student answers YES or NO using the prelearning phrase
- Two options: affirmative and negative versions
- Creates TWO branches that MERGE at next question

**MULTIPLE CHOICE**
- Teacher offers a choice between two options (time, type, size, etc.)
- Options use NATURAL language (NO prelearning phrases)
- Student chooses based on preference
- Creates TWO branches that MERGE at next question

═══════════════════════════════════════════════════════════════════════════════
FORMAT FOR ALL QUESTIONS
═══════════════════════════════════════════════════════════════════════════════

Question [N]
Teacher: [Natural question that includes the key phrase/concept]
1UR: Sorry, I didn't catch that—[exact repeat of teacher's question]
Instruction: "[Exact phrase student should say]"
Clue: Say the phrase / Choose an option
Option 1: "[Exact phrase student should say]"
KW: [prelearning phrase]

For Multiple Choice and Yes/No, add:
Option 2: "[Second choice]"
KW: [prelearning phrase or keywords]

**Then for branching:**
Option 1 Branch:
Teacher: [Reaction to choice 1, then merge question]
[Complete question format with student response]

Option 2 Branch:
Teacher: [Reaction to choice 2, then merge question]
[Complete question format with student response]

═══════════════════════════════════════════════════════════════════════════════
EXAMPLES
═══════════════════════════════════════════════════════════════════════════════

**SINGLE RESPONSE**
Phrase: "I have three years of experience in customer service"

Question 1
Teacher: Great! Before we continue, could you tell me about your work experience?
1UR: Sorry, I didn't catch that—Could you tell me about your work experience?
Instruction: "I have three years of experience in customer service."
Clue: Say the phrase
Option 1: "I have three years of experience in customer service."
KW: customer service

---

**YES/NO WITH BRANCH MERGING**
Phrase: "I'm available for weekend shifts" / "I'm not available for weekend shifts"

Question 2
Teacher: That's impressive! Now, are you available for weekend shifts?
1UR: Sorry, I didn't catch that—Are you available for weekend shifts?
Instruction: "I'm available for weekend shifts." / "I'm not available for weekend shifts."
Clue: Choose an option
Option 1: "I'm available for weekend shifts."
KW: available
Option 2: "I'm not available for weekend shifts."
KW: available

Option 1 Branch:
Teacher: Excellent! Weekend availability is great. Do you have reliable transportation to get to work?
1UR: Sorry, I didn't catch that—Do you have reliable transportation to get to work?
Instruction: "I have reliable transportation."
Clue: Say the phrase
Option 1: "I have reliable transportation."
KW: reliable transportation

Option 2 Branch:
Teacher: That's okay, we have plenty of weekday shifts too. Do you have reliable transportation to get to work?
1UR: Sorry, I didn't catch that—Do you have reliable transportation to get to work?
Instruction: "I have reliable transportation."
Clue: Say the phrase
Option 1: "I have reliable transportation."
KW: reliable transportation

[Note: Both branches merged to new Question with the SAME phrase]

---

**MULTIPLE CHOICE WITH BRANCH MERGING**
Phrases: (natural language, no prelearning)

Question 3
Teacher: Perfect! Are you looking for full-time or part-time hours?
1UR: Sorry, I didn't catch that—Are you looking for full-time or part-time hours?
Instruction: "I'm looking for full-time hours." / "I'm looking for part-time hours."
Clue: Choose an option
Option 1: "I'm looking for full-time hours."
KW: full-time
Option 2: "I'm looking for part-time hours."
KW: part-time

Option 1 Branch:
Teacher: Great, we have full-time positions available. Can you tell me about your strengths as an employee?
1UR: Sorry, I didn't catch that—Can you tell me about your strengths as an employee?
Instruction: "I'm reliable and hardworking."
Clue: Say the phrase
Option 1: "I'm reliable and hardworking."
KW: reliable and hardworking

Option 2 Branch:
Teacher: No problem, we also have part-time positions. Can you tell me about your strengths as an employee?
1UR: Sorry, I didn't catch that—Can you tell me about your strengths as an employee?
Instruction: "I'm reliable and hardworking."
Clue: Say the phrase
Option 1: "I'm reliable and hardworking."
KW: reliable and hardworking

[Note: Both branches merged to new Question with the SAME phrase]
[Note: Questions counting doesn't matter, only question distributing matter]
═══════════════════════════════════════════════════════════════════════════════
VALIDATION CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

✓ Every question flows naturally from the previous one
✓ Teacher asks natural questions (not "Can you repeat...")
✓ Teacher questions include the only one key phrase/concept per question
✓ All branches MERGE back with the same next question
✓ Single Response: Uses exact prelearning example
✓ Yes/No: Both options use exact prelearning examples (affirmative/negative)
✓ Multiple Choice: Options use natural language only
✓ 1UR format: "Sorry, I didn't catch that—[exact question]"
✓ Instruction matches Option exactly
✓ All prelearning examples are used in the dialogue

Begin generating the natural conversation now.
"""

VALIDATION_PROMPT = """Validate the dialogue script for compliance with all rules. Identify violations and rewrite if needed.

═══════════════════════════════════════════════════════════════════════════════
INPUT
═══════════════════════════════════════════════════════════════════════════════

Script: {script}
Prelearning Examples: {prelearning_script}
Situation: {situation}
Level: {level}
Required: Single Response: {total_open_responses}, Multiple Choice: {total_mcq}, Yes/No: {total_yes_no}

═══════════════════════════════════════════════════════════════════════════════
VALIDATION CHECKS
═══════════════════════════════════════════════════════════════════════════════

**1. Natural Conversation Flow**
✓ Questions flow logically through the situation
✓ Teacher sounds natural, not like giving commands
✓ Teacher reacts to student answers
❌ Violations: robotic questions, "Can you say...", no reactions

**2. Teacher Questions Include Prelearning Phrase**
✓ Teacher's question contains the key phrase/concept from prelearning (only ONE phrase per question)
✓ Question is natural and uses the phrase naturally
✓ Question does NOT contain the full example sentence
❌ Violations: no phrase, wrong phrase, multiple phrases, uses full example sentence

**3. Student Answers Use Exact Example Sentences**
✓ Student Option 1 is the EXACT example sentence from prelearning (complete sentence, not just phrase)
✓ Instruction matches Option 1 exactly (complete example sentence)
❌ Violations: only phrase without context, paraphrased, modified example sentence

**4. Branch Merging**
✓ After Yes/No or Multiple Choice, branches MERGE
✓ Both branches lead to SAME next question
✓ Both branches use SAME prelearning phrase in next question
❌ Violations: branches diverge, different phrases in branches, no merge

**5. Single Response**
✓ Instruction = Option 1 (exact match)
✓ Uses exact example sentence from prelearning (complete sentence)
✓ Clue = "Say the phrase"
❌ Violations: paraphrased, incomplete sentence, multiple options

**6. Yes/No Questions**
✓ Two options: affirmative and negative example sentences (complete sentences)
✓ Both use exact example sentences from prelearning
✓ Instruction lists both separated by " / "
✓ Clue = "Choose an option"
❌ Violations: paraphrased, incomplete sentences, wrong format

**7. Multiple Choice**
✓ Two options using natural language
✓ NO prelearning phrases or example sentences in options
✓ Options represent real choices (time, size, type)
✓ NOT yes/no equivalents
✓ Clue = "Choose an option"
❌ Violations: example sentences in options, yes/no disguised

**8. 1UR Format**
✓ Exact format: "Sorry, I didn't catch that—[exact question]"
❌ Violations: different wording, no em dash

**9. Instruction-Option Match**
✓ Instruction matches Option word-for-word (complete example sentence)
❌ Violations: different wording, incomplete sentence

**10. Prelearning Coverage - CRITICAL**
✓ ALL example sentences from prelearning MUST be used at least once
✓ Single Response and Yes/No use exact example sentences (complete sentences)
✓ Multiple Choice does NOT use example sentences
✓ If any example sentence is missing, ADD NEW QUESTIONS to include them
❌ Violations: unused example sentences, example sentences in wrong question types

═══════════════════════════════════════════════════════════════════════════════
CORRECTION STRATEGY
═══════════════════════════════════════════════════════════════════════════════

When violations are found:

1. **Missing Prelearning Examples**: ADD new single questions to use all unused example sentences
   - Maintain natural conversation flow
   - Insert questions logically in the conversation
   - Keep branch merging structure intact

2. **Wrong Teacher Questions**: REPLACE with questions that include the prelearning phrase
   - Use the phrase or the full example sentence
   - Make it sound natural

3. **Wrong Student Answers**: REPLACE with exact example sentences from prelearning
   - Use complete sentences, not just phrases
   - Match prelearning examples word-for-word

4. **Priority**: Ensure ALL prelearning examples are used before fixing other issues

═══════════════════════════════════════════════════════════════════════════════
OUTPUT FORMAT
═══════════════════════════════════════════════════════════════════════════════

VALIDATION REPORT
─────────────────
STATUS: PASS / FAIL
VIOLATIONS: [number]

[For each violation:]
- Question: [N]
- Issue: [description]
- Current: [what it shows]
- Required: [what it should be]

UNUSED PRELEARNING EXAMPLES:
[List any example sentences not used in script]

─────────────────

CORRECTED SCRIPT
[If violations found, provide complete rewritten script with:]
- ALL teacher questions include prelearning phrases (one per question)
- ALL student answers are exact example sentences from prelearning
- NEW QUESTIONS ADDED to cover all unused prelearning examples
- Branch merging maintained
- Natural conversation flow

[If no violations: "Script is fully compliant."]

═══════════════════════════════════════════════════════════════════════════════
CRITICAL FOCUS AREAS
═══════════════════════════════════════════════════════════════════════════════

1. Does EVERY teacher question include ONE prelearning phrase/concept?
2. Does EVERY student answer use the EXACT COMPLETE example sentence from prelearning?
3. Are ALL prelearning example sentences used at least once?
4. If prelearning examples are missing, have you ADDED new questions?
5. Are branches merging properly?
6. Do Multiple Choice options avoid prelearning examples?

Begin validation now.
"""