import sqlite3

DB_NAME = "langue_qcm.db"

# =========================
# LISTE DES QUESTIONS
# =========================
# Chaque élément : (question, niveau, [(texte_choix, correct)])
questions = [

# ================= A1 =================
("I ____ a student.", "A1", [("am",1),("is",0),("are",0),("have",0)]),
("She ____ my friend.", "A1", [("is",1),("am",0),("are",0),("has",0)]),
("They ____ happy.", "A1", [("are",1),("is",0),("am",0),("have",0)]),
("I ____ a cat.", "A1", [("have",1),("has",0),("am",0),("do",0)]),
("He ____ a dog.", "A1", [("has",1),("have",0),("is",0),("does",0)]),
("I ____ not like pizza.", "A1", [("do",1),("does",0),("am",0),("have",0)]),
("She ____ not like apples.", "A1", [("does",1),("do",0),("is",0),("has",0)]),
("The cat is small.", "A1", [("The cat is small",1),("Small is the cat",0),("Cat the small is",0),("Is small the cat",0)]),
("She is a friend.", "A1", [("She is a friend",1),("Friend she is a",0),("Is she a friend",0),("A friend is she",0)]),
("They are happy.", "A1", [("They are happy",1),("Are happy they",0),("Happy they are",0),("They happy are",0)]),
("I have a book.", "A1", [("I have a book",1),("Have I a book",0),("A book I have",0),("Book have I a",0)]),
("He has a dog.", "A1", [("He has a dog",1),("Has he a dog",0),("Dog has he a",0),("Has dog he a",0)]),
("We are at school.", "A1", [("We are at school",1),("Are we at school",0),("At school we are",0),("School are we at",0)]),
("I do like pizza.", "A1", [("I do like pizza",1),("Do I like pizza",0),("Like I do pizza",0),("Pizza like I do",0)]),
("This ____ my pen.", "A1", [("is",1),("are",0),("am",0),("has",0)]),
("These ____ my books.", "A1", [("are",1),("is",0),("am",0),("have",0)]),
("The pen is red.", "A1", [("The pen is red",1),("Red pen the is",0),("Is red the pen",0),("Pen red is the",0)]),
("They are very happy.", "A1", [("They are very happy",1),("Very happy they are",0),("Are happy very they",0),("Happy they are very",0)]),
("I am tired today.", "A1", [("am",1),("is",0),("are",0),("have",0)]),
("We are good friends.", "A1", [("We are good friends",1),("Friends we are good",0),("Good friends we are",0),("Are good friends we",0)]),

# ================= A2 =================
("I have seen that movie.", "A2", [("have",1),("has",0),("did",0),("do",0)]),
("She has finished her homework.", "A2", [("has",1),("have",0),("did",0),("does",0)]),
("I ate breakfast yesterday.", "A2", [("ate",1),("eat",0),("have eaten",0),("do",0)]),
("He played football last weekend.", "A2", [("played",1),("play",0),("plays",0),("has played",0)]),
("Did you do the homework?", "A2", [("do",1),("does",0),("did",0),("have",0)]),
("She went to the shop yesterday.", "A2", [("went",1),("go",0),("gone",0),("has gone",0)]),
("I did my homework yesterday.", "A2", [("I did my homework yesterday",1),("Did I my homework yesterday",0),("My homework I did yesterday",0),("Yesterday I did my homework",0)]),
("I have seen the movie.", "A2", [("I have seen the movie",1),("Seen the movie I have",0),("The movie I have seen",0),("I seen have the movie",0)]),
("He played football yesterday.", "A2", [("He played football yesterday",1),("Played he football yesterday",0),("Football he played yesterday",0),("Yesterday he played football",0)]),
("They have never been to London.", "A2", [("They have never been to London",1),("Never been to London they have",0),("They never have been to London",0),("Have they never been to London",0)]),
("She has just left.", "A2", [("She has just left",1),("Has just she left",0),("Just left she has",0),("She just has left",0)]),
("Did she do the homework?", "A2", [("Did she do the homework",1),("She did the homework?",0),("The homework did she?",0),("Did the homework she?",0)]),
("We have studied English this week.", "A2", [("We have studied English this week",1),("Have we studied English this week",0),("English we have studied this week",0),("This week we have studied English",0)]),
("I lost my keys yesterday.", "A2", [("lost",1),("lose",0),("loses",0),("have lost",0)]),
("Did they play football yesterday?", "A2", [("play",1),("played",0),("plays",0),("have played",0)]),
("He has already done the exercise.", "A2", [("has",1),("have",0),("did",0),("do",0)]),
("She has not finished the project yet.", "A2", [("has",1),("have",0),("did",0),("do",0)]),
("I have never eaten sushi.", "A2", [("have",1),("has",0),("did",0),("do",0)]),
("She called me last night.", "A2", [("called",1),("call",0),("calls",0),("has called",0)]),
("I watched TV yesterday evening.", "A2", [("watched",1),("watch",0),("watches",0),("have watched",0)]),

# ================= B1 =================
("If I ____ more time, I would travel.", "B1", [("had",1),("have",0),("has",0),("do",0)]),
("She wishes she ____ taller.", "B1", [("were",1),("was",0),("is",0),("has",0)]),
("I would go if I ____ enough money.", "B1", [("had",1),("have",0),("has",0),("did",0)]),
("He acts as if he ____ rich.", "B1", [("were",1),("was",0),("is",0)]),
("I would have called you if I ____ your number.", "B1", [("had",1),("have",0),("has",0),("did",0)]),
("I would buy it if I had enough money.", "B1", [("I would buy it if I had enough money",1),("I buy would it if had enough money",0),("If I enough money I would buy it",0),("I if had enough money would buy it",0)]),
("If they had studied harder, they would have passed the exam.", "B1", [("If they had studied harder, they would have passed the exam",1),("Had they studied harder they would have passed",0),("If they studied harder they would pass",0),("They would have passed if studied harder",0)]),
("If I were you, I would not do that.", "B1", [("If I were you, I would not do that",1),("I were you if I would not do that",0),("I would not do that if I were you",0),("You I were if would not do that",0)]),
("He behaves as if he were the boss.", "B1", [("He behaves as if he were the boss",1),("He as if the boss behaves were",0),("Behaves he as if he were the boss",0),("He behaves as he were the boss",0)]),
("I wish I could speak English fluently.", "B1", [("I wish I could speak English fluently",1),("Wish I could speak English fluently",0),("I could speak English fluently wish",0),("I fluently could speak English wish",0)]),
("She looks as if she is worried.", "B1", [("She looks as if she is worried",1),("Looks she as if is worried",0),("She as if looks worried is",0),("As if she is looks worried",0)]),
("I would help you if I understood the instructions.", "B1", [("I would help you if I understood the instructions",1),("Would I help if understood instructions",0),("If I instructions understood I would help",0),("I help would if understood instructions",0)]),
("They would come if they were invited.", "B1", [("were",1),("was",0),("have",0),("do",0)]),
("He would travel more if he had time.", "B1", [("had",1),("have",0),("has",0),("do",0)]),
("She acts like she knows all the answers.", "B1", [("knows",1),("know",0),("knew",0),("has known",0)]),
("He would have passed if he had studied more.", "B1", [("had studied",1),("studied",0),("has studied",0),("study",0)]),
("If it weren't raining, we could play outside.", "B1", [("weren't",1),("wasn't",0),("isn't",0),("hadn't",0)]),
("I would have called if I had your number.", "B1", [("had",1),("have",0),("has",0),("did",0)]),
("She looks as if she has seen a ghost.", "B1", [("She looks as if she has seen a ghost",1),("Looks as if she seen a ghost",0),("She has seen looks as if a ghost",0),("She looks as if seen has a ghost",0)]),

]

# =========================
# INSERTION DANS LA BASE
# =========================
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

for question, niveau, choices in questions:
    cursor.execute(
        "INSERT INTO questions (question, niveau) VALUES (?, ?)",
        (question, niveau)
    )
    q_id = cursor.lastrowid

    for texte, correct in choices:
        cursor.execute(
            "INSERT INTO choices (question_id, texte, correct) VALUES (?, ?, ?)",
            (q_id, texte, correct)
        )

conn.commit()
conn.close()
print("✅ Questions insérées dans la base langue_qcm.db")
