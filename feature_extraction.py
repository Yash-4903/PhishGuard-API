import re
import pandas as pd

def extract_features(url):
    """ Extracts various features from a given URL. """
    if not isinstance(url, str):  # Handle NaN or non-string values
        return {
            "url_length": 0,
            "num_digits": 0,
            "num_special_chars": 0,
            "num_subdomains": 0,
            "https": 0
        }

    features = {
        "url_length": len(url),
        "num_digits": sum(c.isdigit() for c in url),
        "num_special_chars": len(re.findall(r"[\W_]", url)),  # Special characters
        "num_subdomains": url.count("."),
        "https": 1 if url.startswith("https") else 0
    }
    return features

def process_dataset(csv_file):
    df = pd.read_csv(csv_file)

    # Remove NaN values in URL column
    df = df.dropna(subset=["URL"])  

    df["features"] = df["URL"].apply(lambda url: extract_features(url))

    # Convert features dictionary to separate columns
    features_df = pd.DataFrame(df["features"].to_list())

    # Combine original data with extracted features
    final_df = pd.concat([df, features_df], axis=1).drop(columns=["features"])

    return final_df

if __name__ == "__main__":
    processed_data = process_dataset("/Users/yashvardhansinghsolanki/Desktop/Github/PhishGuard/data_collection/phishing_data.csv")
    processed_data.to_csv("processed_data.csv", index=False)
    print(f"✅ Processed {len(processed_data)} URLs and saved feature data!")
