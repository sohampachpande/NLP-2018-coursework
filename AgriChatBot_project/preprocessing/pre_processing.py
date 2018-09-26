from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords as stopwords
import pandas as pd
import csv, operator
import spell_correct_functions
import re

stop_words = set(stopwords.words('english'))

crop_names = pd.read_csv('Cropnames_Indianlanguages.csv')
crop_common_name = crop_names['English']
crop_hindi_name = crop_names['Hindi']
crop_hindi_eng_dict = {}
for eng, hin in zip(crop_common_name,crop_hindi_name):
   crop_hindi_eng_dict.update({str(hin).lower():str(eng).lower()})
#crop_hindi_eng_dict

data =[]

filename = 'data/MH_2017.csv'
with open(filename, 'r') as File: 
    reader = csv.DictReader(File)
    for row in reader:
        data.append(row)
            
ps = PorterStemmer()
wn = WordNetLemmatizer()
df = pd.DataFrame(data)[:]
vocabulary = {}
questions = df['QueryText']
for qi in xrange(len(questions)):
    text = re.findall(r'\w+' ,questions[qi].lower())
    for i in xrange(len(text)):

        if text[i] in crop_hindi_eng_dict.keys():
            text[i] = crop_hindi_eng_dict[text[i]]
        else:
            text[i] = spell_correct_functions.correction(text[i])

        #text[i] = ps.stem(text[i].decode('utf-8'))
        text[i] = wn.lemmatize(text[i].decode('utf-8'))
        
        if text[i] not in stop_words:
            try:
                vocabulary[text[i]] += 1
            except:
                vocabulary[text[i]] = 1
    if len(text) > 0:
        questions[qi] = ' '.join(text)


df1 = df[['QueryText', 'KCCAns']]
df1.drop_duplicates(inplace=True)
df2 =  df1.sort_values(by=['QueryText'])

# Drop Weather Queries
for i in xrange(len(df2)):
    try:
        #print df2.loc[i, 'QueryText']
        if 'weather' in df2.loc[i, 'QueryText'].lower():
            df2.drop(i, inplace=True)
    except:
        None


df2.to_csv('edited_df_for_MH_upto_19.csv')