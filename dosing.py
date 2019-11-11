import argparse
import os
import pandas as pd
import plotly.graph_objects as go

def merge_dataframes(registry_df, ec_df):
    return registry_df.merge(ec_df, 'left', ['RID', 'VISCODE'], suffixes=('', '_ec'))

def filter_dataframe(df, viscode, svdose, ecsdstxt):
    return df[(df['VISCODE'] == viscode) &
              (df['SVDOSE'] == svdose) &
              (df['ECSDSTXT'] != ecsdstxt)].copy()

def create_csv(df, path):
    FILENAME = "results.csv"
    OUTPUT_COLS = ['ID', 'RID', 'USERID', 'VISCODE', 'SVDOSE', 'ECSDSTXT']

    filepath = os.path.join(path, FILENAME)
    df[OUTPUT_COLS].to_csv(filepath, columns=OUTPUT_COLS, index=False)

def generate_csv_report(registry_df, ec_df, viscode, svdose, ecsdstxt, path):
    """
        Generates a CSV report based on filtered results

        Filtered to one VISCODE and SVDOSE 
        One ECSDSTXT is excluded
    """
    df = merge_dataframes(registry_df, ec_df)
    df = filter_dataframe(df, viscode, svdose, ecsdstxt)
    create_csv(df, path)

def generate_pie_chart(registry_df):
    """
        Generates a pie chart of counts of VISCODES

        Filters on Registry dataframe is hardcoded per specification
        Renderer is choosen automatically
    """
    filtered_registry_df = registry_df[(registry_df['SVPERF'] == 'Y') &
                                        (registry_df['VISCODE'] != 'bl')].copy()
    filtered_registry_df.loc[:, 'COUNT'] = 1
    grouped_registry = filtered_registry_df.groupby('VISCODE').count()
    grouped_registry.reset_index(inplace=True)

    fig = go.Figure(go.Pie(
        name = '',
        values = grouped_registry['COUNT'],
        labels = grouped_registry['VISCODE'],
        hovertemplate = "Viscode: <b>%{label}</b><br>Count: <b>%{value}</b> (<b>%{percent}</b>)"
    ))

    fig.update(layout_title_text='Viscodes from Registry')
    fig.show()


if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Generate a pie chart and a CSV file")
    parser.add_argument('--viscode', nargs='?', type=str, default='w02',
        help='One VISCODE to include in the CSV')
    parser.add_argument('--svdose', nargs='?', type=str, default='Y',
        help='One SVDOSE to include in the CSV')
    parser.add_argument('--ecsdstxt', nargs='?', type=int, default=280,
        help='One ECSDSTXT to exclude from the CSV')
    parser.add_argument('--path', nargs='?', type=str, default='.',
        help='Path to output results CSV')

    args = parser.parse_args()
    viscode = args.viscode
    svdose = args.svdose
    ecsdstxt = args.ecsdstxt
    path = args.path

    # Read in the CSV files
    registry_filename = "t2_registry 20190619.csv"
    ec_filename = "t2_ec 20190619.csv"

    registry_df = pd.read_csv(registry_filename)
    ec_df = pd.read_csv(ec_filename)

    # Generate pie chart and csv report
    generate_pie_chart(registry_df)
    generate_csv_report(registry_df, ec_df, viscode, svdose, ecsdstxt, path)
