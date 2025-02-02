from flask import Flask, request, jsonify, render_template
import mlflow
import pickle
import pandas as pd
from urllib.parse import urlparse
import re
import whois
from datetime import datetime
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='static', template_folder='templates')

model = pickle.load(open('xgbClassifier.pkl', 'rb'))

# Feature Extraction Functions
def has_ip(url):
    try:
        domain = urlparse(url).netloc.split(':')[0]
        return 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain) else 0
    except:
        return 0

def has_at(url):
    return 1 if '@' in url else 0

def url_length(url):
    return len(url)

def url_depth(url):
    try:
        path = urlparse(url).path
        return path.count('/')
    except:
        return 0

def has_redirection(url):
    return 1 if url.count('//') > 1 else 0

def https_domain(url):
    return 1 if urlparse(url).scheme == 'https' else 0

def is_tinyurl(url):
    shorteners = {'bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 't.co', 'is.gd', 'buff.ly', 'adf.ly'}
    try:
        domain = urlparse(url).netloc.lower()
        return 1 if any(s in domain for s in shorteners) else 0
    except:
        return 0

def has_prefix_suffix(url):
    try:
        domain = urlparse(url).netloc
        return 1 if '-' in domain else 0
    except:
        return 0

def dns_record(url):
    try:
        domain = urlparse(url).netloc
        w = whois.whois(domain)
        return 1 if w.domain_name else 0
    except:
        return 0

def domain_age(url):
    try:
        domain = urlparse(url).netloc
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        age = (datetime.now() - creation_date).days
        return 0 if age < 365 else 1  # 1 if older than 1 year
    except:
        return 0

def domain_end(url):
    try:
        domain = urlparse(url).netloc
        w = whois.whois(domain)
        expiration_date = w.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        remaining = (expiration_date - datetime.now()).days
        return 1 if remaining < 365 else 0  # 1 if expires within 1 year
    except:
        return 0

def has_iframe(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        return 1 if soup.find('iframe') else 0
    except:
        return 0

def has_mouseover(url):
    try:
        response = requests.get(url, timeout=10)
        return 1 if 'onmouseover' in response.text.lower() else 0
    except:
        return 0

def has_right_click(url):
    try:
        response = requests.get(url, timeout=10)
        return 1 if 'event.button==2' in response.text.lower() else 0
    except:
        return 0

def has_web_forwards(url):
    try:
        response = requests.get(url, timeout=10)
        return 1 if 'meta http-equiv="refresh"' in response.text.lower() else 0
    except:
        return 0

def extract_features(url):
    features = {}
    
    features['Have_IP'] = has_ip(url)
    features['Have_At'] = has_at(url)
    features['URL_Length'] = url_length(url)
    features['URL_Depth'] = url_depth(url)
    features['Redirection'] = has_redirection(url)
    features['https_Domain'] = https_domain(url)
    features['TinyURL'] = is_tinyurl(url)
    features['Prefix/Suffix'] = has_prefix_suffix(url)
    features['DNS_Record'] = dns_record(url)
    features['Domain_Age'] = domain_age(url)
    features['Domain_End'] = domain_end(url)
    features['iFrame'] = has_iframe(url)
    features['Mouse_Over'] = has_mouseover(url)
    features['Right_Click'] = has_right_click(url)
    features['Web_Forwards'] = has_web_forwards(url)
    
    # Web_Traffic (placeholder - needs actual implementation)
    features['Web_Traffic'] = 0  # Replace with actual traffic detection logic
    
    return features

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_url', methods=['POST'])
def predict_from_url():
    try:
        data = request.json
        url = data['url']
        
        if not urlparse(url).scheme:
            url = 'http://' + url
            
        features = extract_features(url)
        
        feature_order = [
            'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection',
            'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic',
            'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over', 'Right_Click', 'Web_Forwards'
        ]
        
        input_df = pd.DataFrame([features])[feature_order]
        
        # Get binary prediction
        prediction = int(model.predict(input_df)[0])
        print(prediction)
        
        # Determine result based on prediction
          # Assuming 0=phishing, 1=legitimate
        is_phishing = prediction
        result_text = "Phishing Website Detected" if prediction == 1 else "Legitimate Website"
        print(result_text)
        
        return jsonify({
            'is_phishing': is_phishing,
            'result': result_text,
            'features': features
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)