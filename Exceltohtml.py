import pandas as pd
import os

path = "in/"
names = []
for filename in os.listdir(path):
    excel_file = f'in/{filename}'
    name = os.path.splitext(filename)[0]
    # Load Excel file into a pandas ExcelFile object
    if name in names:
        raise Exception(f"Duplicate name {name}")
        
    names.append(name)
    xls = pd.ExcelFile(excel_file)

    # List of table names or sheet indices to export
    tables_to_export = ['OutputMatchResults', 'OutputRanking',"OutputQuestions"]  # Replace with your actual table names or indices
    html_file = f"voorspellingen/{name}.html"
    with open(html_file, 'w') as f:
            f.write(f"<h1>{name}</h1></br>")

    for table in tables_to_export:
        # Load table data into a DataFrame
        df = pd.read_excel(xls, table)

        match table:
            case 'OutputMatchResults':
                df["Score Thuis Geworden"] = ["Nvt"]*11
                df["Score Uit Geworden"] = ["Nvt"]*11
                df["Punten"] = [0]*11

            case 'OutputRanking':
                df["Ranglijst"] = [""]*12
                df["Punten"] = [0]*12

            case "OutputQuestions":
                df["Correct"] = [0]*8
                df["Punten"] = [0]*8


        # Convert DataFrame to HTML
        html_output = df.to_html(index=False)

        # Write HTML to a file
        with open(html_file, 'a') as f:
            f.write(html_output)
            f.write("</br>")