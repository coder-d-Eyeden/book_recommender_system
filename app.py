from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open(r'model\popular.pkl','rb'))
pt= pickle.load(open(r'model\pt.pkl','rb'))
books= pickle.load(open(r'model\books.pkl','rb'))
similarity_scores= pickle.load(open(r'model\similarity_scores.pkl','rb'))


app = Flask(__name__)

@app.route('/',methods=['GET','POST'])

def index ():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_rating'].values),
                           rating = list(popular_df['avg_rating'].values)

    )

@app.route("/recommend",methods=['GET','POST'])
def recommend_ui():
        

        if request.method == 'GET':
            return render_template('recommend.html')
        
        user_input = request.form.get('user_input')
        
        if not user_input:
             return render_template(
                  'recommend.html',
                  error = 'Please Enter A Book Name'
             )

        if user_input not in pt.index:
             return render_template('recommend.html',data=[],error=f"'{user_input}'is not available in out database")
        index = np.where(pt.index==user_input)[0][0]
        distances = similarity_scores[index]
        similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
        data =[]
        for i in similar_items:
            item=[]
            temp_df = books[books['Book-Title']==pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)
        
        return render_template('recommend.html',data=data,search_query = user_input)
if __name__ =="__main__":
    app.run(debug=True)
