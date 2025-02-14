import pandas as pd

print("Cleaning up labels.csv")

df = pd.read_csv('data/labels.csv')


df["FlowFileName"] = df["FlowFilePath"].apply(
    lambda path: path[path.find("flows/")+len("flows/"):])


def get_label(label_details):
    return label_details[:label_details.find("packets")-1].strip()


df["Label"] = df["LabelDetails"].apply(
    lambda label_details: get_label(label_details))


df.drop(['LabelDetails', 'FlowFilePath'], axis=1, inplace=True)

print("Writing cleaned up labels.csv to file")

df.to_csv('./data/labels.csv', index=False)

print("Done")
