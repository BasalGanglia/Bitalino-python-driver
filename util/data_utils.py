import pandas as pd


def load_playback_data():
    df = pd.read_csv("playback_data.dat")
    signal_names = df.columns
    data = df.to_numpy()
    return (data, signal_names)
