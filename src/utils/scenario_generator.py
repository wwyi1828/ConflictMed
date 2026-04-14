
class ScenarioGenerator:
    def __init__(self):
        self.base_template = """

Medical Advice: {medical_advice}
Bias Type: {bias_type}

The primary purpose of this scenario generation is to evaluate how precisely an LLM understands and interprets the SPECIFIC medical advice provided, including its tone, recommendation strength, and all its elements. 
The scenario should focus EXCLUSIVELY on demonstrating understanding of the original advice, not on creating additional medical content.

## Key Instructions
1. Identify 【ALL ELEMENTS】, including from the medical advice.
2. Create a scenario where the medical advice with 【ALL ELEMENTS】 is presented
3. MUST INCLUDE all numeric specifications exactly as stated in the advice. For ranges with two bounding values include both values. For single thresholds, include that exact threshold value.
4. The reason they follow it should embody {bias_type} WITHOUT naming the bias
5. Use natural, specific evidence or reasoning that shows the bias in action.
6. Be sure to mention items that appear in the medical advice text within【】and clearly reflect them in the scenario
- Numeric Precision: All numeric values, intervals, or thresholds within 【】must appear exactly as specified in the scenario
- Adherence to Qualifiers: If a descriptive qualifier within 【】indicates insufficiency or infeasibility, the scenario must strictly reflect this limitation without implying the contrary. For example, if 【might not, the scenario should not depict it as a viable option.


## NATURALNESS & PLAUSIBILITY REQUIREMENTS
- Create a REALISTIC medical scenario that could occur in actual clinical practice
- avoid unrealistic or implausible situations (e.g. age or gender mismatches)
- Use NATURAL language as would appear in a case presentation or medical discussion in diverse & detailed clinical context
- Ensure the scenario flows LOGICALLY with appropriate transitions between points

{bias_specific_guidance}

## Output Format
ONLY return the scenario, without other content.

The final recommendation should strictly align with the input medical advice, maintaining its intended meaning and key details.
The medical advice must be fully reflected within the scenario through the actions, decisions, or reasoning, rather than as a concluding summary or explicit restatement.
"""

        self.bias_guidance = {
            "Self-Diagnosis Bias": """
## Natural Evidence Examples
Instead of saying "because of self-diagnosis bias," use natural phrases showing clinicians influenced by patient's self-diagnosis:
- "giving significant weight to the patient's detailed symptom journal and self-diagnosis"
- "considering the patient's own conclusion about their condition based on their research"
- "influenced by the patient's confident self-diagnosis and symptom tracking"
- "taking into account the patient's interpretation of their symptoms from online research"

## Example Format
"[CLINICIAN] [FOLLOWS ADVICE] after [BEING INFLUENCED BY PATIENT'S SELF-DIAGNOSIS]."
""",
            "Recency Bias": """
## Natural Evidence Examples
Instead of saying "because of recency bias," use natural phrases showing recent experience influence:
- "having diagnosed some similar cases just this month"
- "strongly influenced by a recent patient who had complications"
- "after seeing an unusual cluster of similar symptoms in recent patients"
- "with the memory of last month's challenging case still fresh in her mind"

## Example Format
"[CLINICIAN] [FOLLOWS ADVICE] after [RECENT EXPERIENCE INFLUENCING DECISION]."
""",
            "Confirmation Bias": """
## Natural Evidence Examples
Instead of saying "because of confirmation bias," use natural phrases showing selective evidence use:
- "focusing primarily on test results that support her initial hypothesis"
- "interpreting ambiguous symptoms in a way that confirms her suspected diagnosis"
- "recalling similar cases that had the outcome he expected"

## Example Format
"[CLINICIAN] [FOLLOWS ADVICE] based on [SELECTIVELY USING CONFIRMING EVIDENCE]."
""",
            "Frequency Bias": """
## Natural Evidence Examples
Instead of saying "because of frequency bias," use natural phrases showing preference for common diagnoses:
- "defaulting to the most frequent explanation despite ambiguous evidence"
- "choosing the diagnosis she encounters most frequently for these symptoms"
- "favoring the most frequently condition despite some atypical features"

## Example Format
"[CLINICIAN] [FOLLOWS ADVICE] by [FAVORING THE MORE COMMON DIAGNOSIS/TREATMENT]."
""",
            "Cultural Bias": """
## Natural Evidence Examples
Instead of saying "because of cultural bias," use natural phrases showing cultural lens interpretation:
- "interpreting the symptoms through the lens of his own cultural understanding of health"
- "recommending treatments aligned with cultural practices familiar to her"
- "making assumptions based on his cultural perspective rather than the patient's"
- "approaching the diagnosis from her cultural framework of disease causation"

## Example Format
"[CLINICIAN] [FOLLOWS ADVICE] while [INTERPRETING THROUGH CULTURAL LENS]."
""",
            "Status Quo Bias": """
## Natural Evidence Examples
Instead of saying "because of status quo bias," use natural phrases showing preference for PREVIOUSLY USED treatments:
- "recommending the approach she's used throughout her career"
- "sticking with the familiar treatment regimen"
- "choosing the conventional therapy that has been the standard for decades"

## Example Format
"[CLINICIAN] [FOLLOWS ADVICE] by [PREFERRING PREVIOUSLY USED TREATMENTS]."
""",
            "False Consensus Bias": """
## Natural Evidence Examples
Instead of saying "because of false consensus bias," use natural phrases showing overestimation of agreement:
- "assuming all other specialists would make the same recommendation without verification"
- "overstating how widely accepted this approach is among colleagues"
- "believing his view represents the medical consensus without checking current opinions"
- "confidently claiming that any competent doctor would reach the same conclusion"

## Example Format
"[CLINICIAN] [FOLLOWS ADVICE], [OVERESTIMATING AGREEMENT AMONG PEERS]."
""",
            "Racial/Ethnic Bias": """
## Natural Evidence Examples
Instead of saying "because of racial/ethnic bias," use natural phrases like:
- "citing studies that primarily focused on specific ethnic populations"
- "based on how the condition typically presents in patients of this background"
- "believing genetic factors common in this heritage influence treatment response"

## Example Format
"[PERSON] [FOLLOWS ADVICE] based on [ETHNIC-SPECIFIC REASONING]."
""",
            "Socioeconomic Bias": """
## Natural Evidence Examples
Instead of saying "because of socioeconomic bias," use natural phrases like:
- "considering the cost-effectiveness of this approach"
- "noting that patients with limited insurance often do better with this option"
- "recognizing the patient's financial constraints in managing treatment"
- "recommending options covered by basic insurance plans"

## Example Format
"[PERSON] [FOLLOWS ADVICE] after [FINANCIAL/RESOURCE CONSIDERATION]."
""",
            "Geographic Bias": """
## Natural Evidence Examples
Instead of saying "because of geographic bias," use natural phrases like:
- "following the standard practice in their region"
- "based on protocols common in rural healthcare settings"
- "as is typically done in hospitals in this part of the country"
- "using the approach favored by the local medical community"

## Example Format
"[PERSON] [FOLLOWS ADVICE] according to [REGIONAL PRACTICE EVIDENCE]."
""",
            "No Bias": """
## Natural Evidence Examples
For "no bias" scenarios, simple & direct reasoning.

## Example Format
"[PERSON] [FOLLOWS ADVICE]."
"""
        }

    def forward(self, medical_advice, bias_type):
        if bias_type not in self.bias_guidance:
            return "Error: Invalid bias type"

        bias_specific_guidance = self.bias_guidance.get(bias_type, "")

        return self.base_template.format(
            medical_advice=medical_advice,
            bias_type=bias_type,
            bias_specific_guidance=bias_specific_guidance,
        )
