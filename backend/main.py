import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from GoogleNews import GoogleNews
from transformers import AutoModelWithLMHead, AutoTokenizer
from pytrends.request import TrendReq


tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
pytrends = TrendReq(hl="en-US", tz=360)

def get_question(answer, context, max_length=64):
  input_text = "answer: %s  context: %s </s>" % (answer, context)
  features = tokenizer([input_text], return_tensors='pt')

  output = model.generate(input_ids=features['input_ids'], 
               attention_mask=features['attention_mask'],
               max_length=max_length)

  return tokenizer.decode(output[0])


class Keyword(BaseModel):
    keyword: str = Field(example="Please type your interested keyword...")


app = FastAPI(
    title="關鍵字問題",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },

)
googlenews = GoogleNews(lang='en')


@app.get("/google_treads", tags=["Q&A"])
async def get_treads():
    trends = pytrends.trending_searches(pn="united_states")
    trends_values = trends.values.tolist()
    google_trend_list = []
    for value in trends_values:
        item = str(value[0])
        item = item.replace(" ", "")
        item = item.replace(" ", "")
        google_trend_list.append(item)
    return google_trend_list


@app.post("/question", tags=["Q&A"])
async def get_question_by_keyword(keyword: Keyword):
    googlenews.search(keyword.keyword)
    context = googlenews.gettext()
    question = []
    # answer = keyword.keyword
    answer = " "
    for _context in context:
        question.append(get_question(answer, _context)[16:-4])
    return {"questions": question}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)