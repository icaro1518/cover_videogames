import pandas as pd
from sodapy import Socrata

client = Socrata("www.datos.gov.co", None)

results = client.get_all("he3q-86dn")

# Convertir a DataFrame pandas
results_df = pd.DataFrame.from_records(results)

# Guardar como CSV
results_df.to_csv("data/raw_data.csv", index=False)