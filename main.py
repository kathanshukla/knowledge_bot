# import main
import streamlit as st
from langchain.chains import ConversationChain
from langchain_community.llms import GooglePalm
from dotenv import load_dotenv
import os
import google.generativeai as palm
from langchain_google_genai import GoogleGenerativeAI
import database
from langchain.memory import ConversationEntityMemory
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE


# loading the environent
load_dotenv()

#configuring the APIs
mongo_url = os.getenv('mongo_url')
api_key = os.getenv('GOOGLE_API_KEY')
palm.configure(api_key = os.getenv('GOOGLE_API_KEY'))

llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.5)

qa_retriever = database.vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2},
)


prompt_template = """
Use the following context (delimited by <ctx></ctx>) and the chat history (delimited by <hs></hs>) to answer the question:
----------
<ctx>
{context}
</ctx>
----------
<hs>
{history}
</hs>
----------
{question}
Answer:
"""


memory = ConversationBufferMemory(
    memory_key = "history",
    input_key="question"
)




PROMPT = PromptTemplate(
    input_variables=["history", "context","question"],
    template=prompt_template
)


qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever= qa_retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT,"memory":memory}
)

def get_answer(question):
    question = question
    # chat_message_history.add_user_message(question)
    docs = qa.invoke({"query": question})
    answer = docs["result"]
    return answer



if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

def get_text():
    """
    Get the user input text.
    Returns:
    (str): The text entered by the user
    """
    input_text = st.text_input("You:", st.session_state["input"],key="input",
                                placeholder="Your AI assistant here! Ask me anything ...",
                                label_visibility='hidden')

    return input_text

st.title("Knowledge Bot🧠")
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.9)

if 'enity_memory' not in st.session_state:
    st.session_state.entity_memory = ConversationEntityMemory(llm=llm,k=10)

Conversation = ConversationChain(
    llm=llm,
    prompt = ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory = st.session_state.entity_memory
)


# Get the user input
user_input = get_text()

if user_input:
    # output = Conversation.run(input=user_input)
    output = get_answer(user_input)
    
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

with st.expander("Conversation"):
    for i in range(len(st.session_state['generated'])-1,-1,-1):
        st.info(st.session_state["past"][i],icon="🙎🏻‍♂️")
        st.success(st.session_state["generated"][i],icon="🤖")
with st.sidebar:
    with st.expander("All policies"):    
        st.title("Policies")
        status = st.radio("Select one: ", ('LIC', 'SBI'))    
        if (status == 'LIC'):
            st.success("These all are the policies of LIC")
            st.info("LIC Endowment Plan ")
            # st.write("[- LIC’s Dhan Vriddhi \n(UIN: 512N362V02)](%s)" %url)
            st.markdown("- [LIC’s Dhan Vriddhi \n(UIN: 512N362V02)](%s)"%"https://drive.google.com/file/d/1EDf4TnDdPtub5FGZKSZGmEsok6UX80un/view?usp=sharing")
            st.markdown("- [LIC’s JEEVAN LABH (UIN: 512N304V02)](%s)" %"https://drive.google.com/file/d/1LYWn06wNKv95WU-6oztOKNdzMBUFeDWQ/view?usp=sharing")
            st.markdown("- [LIC’s NEW ENDOWMENT PLAN (UIN: 512N277V02)](%s)"%"https://drive.google.com/file/d/1xIv_i-OeH8pLGcawb2REQcm3gFB9XACp/view?usp=sharing")
            st.markdown("- [LIC’S SINGLE PREMIUM ENDOWMENT PLAN(UIN: 512N283V02)](%s)"%"https://drive.google.com/file/d/1LvjX6fDEb6j9En8w0kujzHytZCHSzdHl/view?usp=sharing")
            st.markdown("- [LIC’s NEW JEEVAN ANAND PLAN (UIN: 512N279V02 )](%s)"%"https://drive.google.com/file/d/16r8SCjz5vPDj41fVhYQIY7E24A4Lvmwk/view?usp=sharing")
            st.markdown("- [LIC’s JEEVAN LAKSHYA (UIN: 512N297V02)](%s)"%"https://drive.google.com/file/d/1EjZFKVKwY633u8D-Oz4JDpFUQyp8U6om/view?usp=sharing")
            st.markdown("- [LIC’s BIMA JYOTI (UIN: 512N339V02)](%s)"%"https://drive.google.com/file/d/1EjZFKVKwY633u8D-Oz4JDpFUQyp8U6om/view?usp=sharing")
            st.markdown("- [LIC’s Aadhaar Shila (UIN: 512N309V03)](%s)"%"https://drive.google.com/file/d/1XbzagxNVs4443t7m6XBiagTCqK__tB5F/view?usp=sharing")
            st.markdown("- [LIC’s Aadhaar Stambh (UIN: 512N310V03)](%s)"%"https://drive.google.com/file/d/1N4sMfVhsEVtSJ8Ef5CILu9gNXfj215jD/view?usp=sharing")
            st.markdown("- [LIC’s Jeevan Azad (UIN: 512N348V01)](%s)"%"https://drive.google.com/file/d/1rJmXHWJCaY7Uu-4xVlC9Vlk_3IZKJZLU/view?usp=sharing")
            st.markdown("- [LIC’s Dhan Sanchay (UIN: 512N346V01 )](%s)"%"https://drive.google.com/file/d/1Kp070ndS_9N5idGfJE-aJbGDSNmHssos/view?usp=sharing")
            st.markdown("- [LIC’s Bima Ratna (UIN: 512N345V01)](%s)"%"https://drive.google.com/file/d/1fLo0HOa1nq8dbjnuK4_r_mk4QGjepZwh/view?usp=sharing")
            st.info("LIC Money back plan ")
            #money back plan
            st.markdown("- [LIC’S NEW BIMA BACHAT (UIN:512N284V02)](%s)"%"https://drive.google.com/file/d/1dzTgCocBJKD76Oa3lS4pwzCevUI8FqfC/view?usp=sharing")
            st.markdown("- [LIC’s NEW CHILDREN’s MONEY BACK PLAN (UIN: 512N296V02)](%s)"%"https://drive.google.com/file/d/17B9_RiQgVLpYmfrXVP5WVwjIUms66jva/view?usp=sharing")
            st.markdown("- [LIC’s Jeevan Shiromani (UIN:512N315V02 )](%s)"%"https://drive.google.com/file/d/1ZkhtZ-ONuWYlwDrWliR2TQrD0_hqkKw_/view?usp=sharing")
            st.markdown("- [LIC’s Bima Shree (UIN: 512N316V02 )](%s)"%"https://drive.google.com/file/d/1BBcIGxxSIilQbLUPnyUrbzBZ9EywdZoO/view?usp=sharing")
            st.markdown("- [LIC’s JEEVAN UMANG (UIN:512N312V02)](%s)"%"https://drive.google.com/file/d/10BLXw1YICfsa7pvr0dIAewLxu6sbzvFw/view?usp=sharing")
            st.markdown("- [LIC’s NEW MONEY BACK PLAN – 25 YEARS (UIN:512N278V02)](%s)"%"https://drive.google.com/file/d/18rXSzebGzTDYRk84NZ2m0lPfeZyOKx94/view?usp=sharing")
            st.markdown("- [LIC’s NEW MONEY BACK PLAN – 20 YEARS (UIN:512N280V02)](%s)"%"https://drive.google.com/file/d/1WbwkhtRlSGNYleQ_gx2CkbWG4DrHrmy1/view?usp=sharing")
            st.markdown("- [LIC’s JEEVAN TARUN (UIN: 512N299V02)](%s)"%"https://drive.google.com/file/d/14LhuvVEoK9_WNxLdRtR9R3Uiilrcvdrp/view?usp=sharing")
            st.markdown("- [LIC’s Dhan Rekha (UIN: 512N343V01)](%s)"%"https://drive.google.com/file/d/1CphV3ZFmho-BJSj-U5HD9W74S4N8zVHt/view?usp=sharing")
            st.info("Riders ")
            st.markdown("- [LIC’s Linked Accidental Death Benefit Rider (UIN: 512A211V02)](%s)"%"https://drive.google.com/file/d/1c1pvD4KbIPc_2B8LYvkcWSJR9Fusz-D1/view?usp=sharing")
            st.markdown("- [LIC’s New Term Assurance Rider (UIN: 512B210V01)](%s)"%"https://drive.google.com/file/d/1-6_K3UtIM-YwfuRoORoyT8YHyVqkI7jD/view?usp=sharing")
            st.markdown("- [LIC’s PREMIUM WAIVER BENEFIT RIDER (UIN: 512B204V03)](%s)"%"https://drive.google.com/file/d/1ulhxNnYHa1M1zNxvdcfUQB7XxbP4B4zV/view?usp=sharing")
            st.markdown("- [LIC’s Accident Benefit Rider (UIN: 512B203V03)](%s)"%"https://drive.google.com/file/d/1kKJYscv6iGttLJcjrLvJyLIjMapBYxs1/view?usp=sharing")
            st.markdown("- [LIC’s Accidental Death and Disability Benefit Rider (UIN: 512B209V02)](%s)"%"https://drive.google.com/file/d/1Cv-5VjNPN-LXSZhgTUiyUbYb82x8rG7L/view?usp=sharing")
            st.markdown("- [PREMIUM WAIVER BENEFIT RIDER (WITH AUTO COVER)](%s)"%"https://drive.google.com/file/d/1x7fhBCD37WvhITc-GNey4Ysi2aKaratW/view?usp=sharing")
            st.markdown("- [LIC’s New Critical Illness Benefit Rider (UIN: 512A212V02)](%s)"%"https://drive.google.com/file/d/1vms9_UPHeOQkaqPUOkefs2bfPV0G5pb-/view?usp=sharing")
            st.info("Term assurance plan")
            #term assurance plan
            st.markdown("- [LIC’s Jeevan Kiran (UIN: 512N353V01)](%s)"%"https://drive.google.com/file/d/1CGZDVgOqA9M3s--MhPGTKzvIjDRwUjMQ/view?usp=sharing")
            st.markdown("- [LIC’s New Jeevan Amar (UIN:512N350V01)](%s)"%"https://drive.google.com/file/d/1L5mRz3nWSSZK1h-724JymHGMRvqY8kdR/view?usp=sharing")
            st.markdown("- [LIC’s New Tech-Term (UIN: 512N351V01)](%s)"%"https://drive.google.com/file/d/1_6YASaield3Wrwvha16Y5UmN2sgJvWZ3/view?usp=sharing")
            st.markdown("- [LIC’s Saral Jeevan Bima (UIN: 512N341V01)](%s)"%"https://drive.google.com/file/d/1AyAIkP4gtE8ow5gfHs9oMw10ZcakNCGB/view?usp=sharing")
            st.info("Whole Life Plan  ")
            #whole life plan
            st.markdown("- [LIC’s JEEVAN UMANG (UIN:512N312V02)](%s)"%"https://drive.google.com/file/d/1fX-UQN9Mwfo7_468FrfijeX50JHconeE/view?usp=sharing")
            st.markdown("- [LIC’s Jeevan Utsav (UIN:512N363V01)](%s)"%"https://drive.google.com/file/d/1CrEqRKcIopmfJQ44hJMSFDEIVcjyGmQb/view?usp=sharing")

        else:
            st.success("These all are the policies of SBI")
            st.markdown("- [SBI Life Sampoorn Cancer Suraksha](%s)"%"https://drive.google.com/file/d/1Wob3YM4438ybpYskOOqtPmlvh-F91Azv/view?usp=sharing")
            st.markdown("- [Saral Swadhan Supreme](%s)"%"https://drive.google.com/file/d/1mdiOM6HmJtTVL28BJclPS9SlnW4VFDGN/view?usp=sharing")
            st.markdown("- [eWelth](%s)"%"https://drive.google.com/file/d/199j5-OqRz4Be6yfIDlFpiMppBNEdzQqQ/view?usp=sharing")
            st.markdown("- [New Smart Samriddhi](%s)"%"https://drive.google.com/file/d/15pWS86Eim9ENNM978xqnjDaugLSrgF9I/view?usp=sharing")
            st.markdown("- [Reretire Smart Plus](%s)"%"https://drive.google.com/file/d/1xuctj-oWYhNs8WFrhTKzvsNalBti7OKx/view?usp=sharing")
            st.markdown("- [Saral Jeevan Bima](%s)"%"https://drive.google.com/file/d/1DxlWkaFH4Mps3wuKMAj3K-TDqHQYHvIs/view?usp=sharing")
            st.markdown("- [Smart Annuity Plus](%s)"%"https://drive.google.com/file/d/1MB7XIHRT2Tgp_kKQsv12RZN65BchBvp_/view?usp=sharing")
            st.markdown("- [Smart Platina Assure](%s)"%"https://drive.google.com/file/d/1sCSnCDuAibNbm_nH2naSyWZqUg_AgwRH/view?usp=sharing")
            st.markdown("- [Smart Platina Plus](%s)"%"https://drive.google.com/file/d/1G04t0B37ADCQOCGtP5iVcD004WM4xMCX/view?usp=sharing")
            st.markdown("- [eShild Next](%s)"%"https://drive.google.com/file/d/1ksii8rP5PckJVbBxwgL0abiWkHZjDBng/view?usp=sharing")
            st.markdown("- [Smart Champ Insurance](%s)"%"https://drive.google.com/file/d/1g0tZhNEz592Jbhx9_4iys1tIB0Mjl1gr/view?usp=sharing")
            st.markdown("- [Smart Swadhan Supreme](%s)"%"https://drive.google.com/file/d/1HgDL0eeKm_wJLIi5ikO2Ag4UKab2cufN/view?usp=sharing")
            st.markdown("- [Smart Wealth Builder](%s)"%"https://drive.google.com/file/d/1gIj-Jc8A30rJEWSgRDjBLBwJL6l4PCVM/view?usp=sharing")
            st.markdown("- [Smart Champ Insurance](%s)"%"")

            

        
