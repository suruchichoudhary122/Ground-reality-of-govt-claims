🇮🇳 AI to Detect Policy vs Practice Gaps in Government Schemes
🤖 An NLP-based project to identify contradictions between government policy claims and ground reality reports using Natural Language Inference (NLI).

📌 Problem Statement
Government press releases and scheme dashboards often present highly optimistic data. However, field reports, journalistic articles, and citizen complaints frequently contradict these claims.

This project aims to automate the detection of such contradictions using Natural Language Processing (NLP) and transformer-based NLI models.

🧠 Objective
Extract government claims from official sources (e.g., PIB, MyGov)
Collect real-world reports from news articles, surveys, or social media
Use a pretrained NLI model to classify the relationship between claim and report as:

  ✅ Fulfilled

  ❌ Unfulfilled

  🤷 Unclear

📁 Dataset
📄 1. govt_claims.csv
  Contains official government scheme statements.
  csvid	scheme	claim_text	state	district	source	date
          1	Har Ghar Jal	5.38 Cr households provided tap water since 2019	All India	All Districts	PIB	2021-12-05
📄 2. ground_reality.csv
  Contains real-world reports from credible sources.
  csvid	scheme	report_text	state	district	source	type
          1	Har Ghar Jal	Women in Bundelkhand walk 2 km daily to fetch water	Uttar Pradesh	Banda	WaterAid	field_report

🔧 Tools & Libraries
transformers (HuggingFace)
facebook/bart-large-mnli (zero-shot NLI model)
pandas
tqdm
Google Colab / Jupyter Notebook

⚙️ How It Works
Merge each government claim with related ground reports (by scheme/state)

Run NLI model with:
          premise = claim_text
          hypothesis = report_text

Classify into:

  ENTAILMENT → Fulfilled
  CONTRADICTION → Unfulfilled
  NEUTRAL → Unclear

Output stored in classified_policy_gap_output.csv

📊 Sample Output
scheme	claim_text	report_text	final_label	confidence
Har Ghar Jal	All homes now have tap water	Women still walk 2 km in Banda for water	Unfulfilled	0.91

✅ Project Highlights
      🧠 Uses advanced NLI transformer model (facebook/bart-large-mnli)
      
      📰 Combines structured government data with unstructured reports
      
      📚 Real-world, impactful use-case: accountability through AI
      
      📈 Can be extended to dashboards, visualizations, or alert systems

🔮 Future Improvements
  Fine-tune NLI model on Indian policy + RTI data
  Integrate tweet/news scrapers for live updates
  Add a Streamlit dashboard to view fulfilled/unfulfilled maps
  Use geolocation for more granular analysis

🙌 Acknowledgements
  Government Data via PIB.gov.in
  Field reports from WaterAid, The Wire, NDTV, DownToEarth, Scroll.in, etc.
  NLP tools by HuggingFace Transformers
  
