import pandas as pd

ngkolmpu_df = pd.read_csv("data/ngkolmpu_data_example.csv")

def i_sig (sig, pos, form, lex, df):
    dist = df[df[pos] == form]
    dist_sig = set(dist[sig][dist.l_0 == lex])
    v_sig = set(df[sig])
    I_sig = set()
    if dist_sig < v_sig:
        I_sig = dist_sig
    return I_sig



def i_sig_all (pos, form, lex, df):
    i_sig_all_out = {}
    for sig in [col for col in df if col.startswith('c_')]: #We could define this as a variable outside the function at some point along with the values.:
        i_sig_all_out[sig] = i_sig(sig, pos, form, lex, df)
    return i_sig_all_out



def lexAnalyse(lex, df):
    para = {}

    for pos in [col for col in df if col.startswith('f_')]:
        forms = df[pos].unique()

        for form in forms:
            if pd.isna(form):
                pass
            else:
                posform = (pos, form)
                para[posform] = i_sig_all(pos, form, lex, df)
            
    return para


def classify_VE(lex, df):
    table = []

    formval = lexAnalyse(lex, df)

    for word in df.iloc:

        formatives = []
        for pos in [col for col in df if col.startswith('f_')]:

            if pd.isna(word[pos]):
                pass
            else:
                posform = (pos, word[pos])
                formatives.append(posform)

        for pair in [(formatives[i],formatives[j]) for i in range(len(formatives)) for j in range(i+1, len(formatives))]:
            cell = set()
            for sig in [col for col in df if col.startswith('c_')]:
                cell.add(word[sig])
                forma = pair[0] #('f_s3', 'ai')
                formb = pair[1]
                if formval[forma][sig] & formval[formb][sig]:
                    if formval[forma][sig] == formval[formb][sig]:
                        typ = 'ME'
                    elif formval[forma][sig].issubset(formval[formb][sig]) or formval[formb][sig].issubset(formval[forma][sig]):
                        typ = 'SE'
                    else:
                        typ = 'DE'

                    table.append({'Wordform': word['wordform'],
                                  'Cell': cell,
                                  'Value': word[sig],
                                    'FormA':forma,
                                    'FormB':formb,
                                    'Type': typ})
    return table
