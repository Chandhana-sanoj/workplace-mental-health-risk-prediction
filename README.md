# workplace-mental-health-risk-prediction
Live app → (https://workplace-mental-health-risk-prediction.streamlit.app/)

A Machine Learning web application that predicts whether a tech industry employee may benefit from mental health support, based on workplace conditions and personal factors. Built using the OSMI Mental Health in Tech Survey (2014 + 2016).

## Demo

![Application Demo](screenshots/demo.gif)

## Dataset

The 2014 and 2016 OSMI surveys used completely different column formats — this project includes a schema mapping pipeline to align both years into one clean dataset.

- 2,679 survey responses
- 55 duplicate records identified and removed
- Final dataset: 2,607 survey responses
- 16 features across demographic, company, and workplace categories
- Target: `treatment`(sought mental health support — Yes/No)
- Class balance: ~55% Yes / ~45% 

## Pipeline

- Schema mapping across two survey years
- Value alignment, Gender standardisation, Age filtering
- Data quality assessment (missing values and duplicate detection)
- Train-test split before encoding — no data leakage
- OrdinalEncoder, OneHotEncoder, LabelEncoder, MinMaxScaler
- 6 models compared, optimised for Recall
- Deployed as Streamlit web app

## Results

| Model | Recall | F1 | Accuracy |
|--------|--------|----|-----------|
| Logistic Regression (Tuned) | 0.798 | 0.751 | 0.709 |
| XGBoost (Tuned) | 0.774 | 0.732 | 0.690 |
| Random Forest (Tuned) | 0.753 | 0.736 | 0.703 |
| KNN | 0.645 | 0.673 | 0.655 |
| Naive Bayes | 0.568 | 0.631 | 0.634 |
| Decision Tree | 0.638 | 0.639 | 0.603 |

Recall was the primary metric — missing someone who needs support is worse than a false alarm.

## Tech Stack

Python • Pandas • NumPy • Scikit-Learn •  Streamlit  • GitHub

## Reference
Paul, M. & Das, S. (2023). Mental health in tech workplace: An analysis. IJSRA, 10(01), 221–233. (https://doi.org/10.30574/ijsra.2023.10.1.0743)

## Ethical Note

This tool is intended as a screening aid only — not a medical diagnosis. Always involve qualified professionals in mental health decisions.


