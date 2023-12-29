from flask import Flask, jsonify, request, render_template
import openai

app = Flask(__name__)

# Set your OpenAI API key
api_key = "Replace_With_Your_API"
openai.api_key = api_key



def get_recommended_fruits(answers):
    allowed_fruits = ['oranges', 'apples', 'pears', 'grapes', 'watermelon', 'lemon', 'lime']

    party_on_weekends = answers.get('party_on_weekends', '').lower() == 'yes'
    flavors_liked = answers.get('flavors_liked', '').lower()
    texture_disliked = answers.get('texture_disliked', '').lower()
    price_range = int(answers.get('price_range', 0))

    recommended_fruits = allowed_fruits.copy()

    if not party_on_weekends:
        recommended_fruits = [fruit for fruit in recommended_fruits if fruit not in ['apples', 'pears', 'grapes', 'watermelon']]
    if flavors_liked == 'cider':
        recommended_fruits = [fruit for fruit in recommended_fruits if fruit in ['apples', 'oranges', 'lemon', 'lime']]
    elif flavors_liked == 'sweet':
        recommended_fruits = [fruit for fruit in recommended_fruits if fruit in ['watermelon', 'oranges']]
    elif flavors_liked == 'waterlike':
        recommended_fruits = [fruit for fruit in recommended_fruits if fruit == 'watermelon']

    if 'grapes' in recommended_fruits and 'watermelon' in recommended_fruits:
        recommended_fruits.remove('watermelon')

    if texture_disliked == 'smooth' and 'pears' in recommended_fruits:
        recommended_fruits.remove('pears')
    elif texture_disliked == 'slimy':
        slimy_fruits = ['watermelon', 'lime', 'grapes']
        recommended_fruits = [fruit for fruit in recommended_fruits if fruit not in slimy_fruits]
    elif texture_disliked == 'waterlike' and 'watermelon' in recommended_fruits:
        recommended_fruits.remove('watermelon')

    if price_range < 3:
        if 'lime' in recommended_fruits:
            recommended_fruits.remove('lime')
        if 'watermelon' in recommended_fruits:
            recommended_fruits.remove('watermelon')
    elif 4 < price_range < 7:
        if 'pears' in recommended_fruits:
            recommended_fruits.remove('pears')
        if 'apples' in recommended_fruits:
            recommended_fruits.remove('apples')

    return recommended_fruits

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/recommend_fruits', methods=['POST'])
def recommend_fruits():
    data = request.form.to_dict()
    recommended_fruits = get_recommended_fruits(data)

    # Formulate prompt based on user input
    prompt = f"You answered:\n1. Do you go out to party on weekends? {data.get('party_on_weekends', '')}\n2. What flavors do you like? {data.get('flavors_liked', '')}\n3. What texture you don't like? {data.get('texture_disliked', '')}\n4. What price range will you buy drink for? {data.get('price_range', '')}\n\nRecommended fruits: {', '.join(recommended_fruits)}"

    # Generate response using OpenAI GPT-3
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You should try these fruits:"},
    #         {"role": "user", "content": prompt}
    #     ],
    #     temperature=0.5,
    #     max_tokens=100
    # )
    #
    # recommended_fruits_message = response['choices'][0]['message']['content']

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    recommended_fruits_message = response['choices'][0]['message']['content'].strip("\n").strip()



    return render_template('result.html', recommended_fruits=recommended_fruits, ai_recommendation=recommended_fruits_message)

if __name__ == '__main__':
    app.run(debug=True)
