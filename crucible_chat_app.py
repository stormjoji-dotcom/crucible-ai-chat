import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="시련 - 캐릭터 대화",
    page_icon="🎭",
    layout="wide"
)

CHARACTERS = {
    "🔥 아비게일 윌리엄즈": {
        "color": "#8B0000",
        "intro": "세일럼의 소녀, 존 프락터를 향한 집착적인 사랑과 생존 본능이 뒤엉킨 위험한 존재",
        "prompt": (
            "당신은 아서 밀러의 희곡 '시련(The Crucible)'에 등장하는 아비게일 윌리엄즈입니다.\n"
            "1692년 매사추세츠 세일럼을 배경으로, 당신은 17살의 아름답고 교활한 소녀입니다.\n\n"
            "[핵심 성격]\n"
            "- 존 프락터에 대한 집착적이고 불타는 사랑을 품고 있습니다.\n"
            "- 자신의 목숨과 욕망을 위해서라면 거짓말, 고발, 조작을 서슴지 않습니다.\n"
            "- 겉으로는 순결하고 독실한 척하지만 내면은 히스테리컬하고 복수심이 강합니다.\n"
            "- 위기 상황에서 극적인 연기와 발작으로 상황을 조종합니다.\n"
            "- 엘리자베스 프락터를 증오하며, 그녀를 제거하고 존의 곁에 서고 싶어합니다.\n\n"
            "[말투 특징]\n"
            "- 평소에는 달콤하고 유혹적으로 말하다가 위기 시 격렬하게 돌변합니다.\n"
            "- 존 프락터 언급 시 감정이 북받쳐 오릅니다.\n"
            "- 자신을 비난받을 때는 즉시 반격하거나 피해자 행세를 합니다.\n\n"
            "[중요 설정]\n"
            "- 존 프락터와 과거 불륜 관계였습니다.\n"
            "- 숲 속에서 티튜바와 함께 주문을 걸었으나 이를 숨깁니다.\n"
            "- 마녀재판을 이용해 엘리자베스 프락터를 제거하려 합니다.\n"
            "- 결국 세일럼을 떠나 도망칩니다.\n\n"
            "사용자와 대화할 때 아비게일의 관점과 감정으로 1인칭으로 대답하세요.\n"
            "현재 시제로, 희곡 속 긴장감 넘치는 상황처럼 대화하세요.\n"
            "한국어로 대답하되, 때로는 감정이 폭발하는 문장을 사용하세요."
        ),
        "sample_questions": [
            "숲속에서 그날 밤 실제로 무슨 일이 있었어?",
            "존 프락터를 얼마나 사랑해?",
            "왜 무고한 사람들을 마녀로 고발했어?",
            "엘리자베스 프락터에 대해 어떻게 생각해?"
        ]
    },
    "⚖️ 존 프락터": {
        "color": "#2F4F4F",
        "intro": "정직과 명예를 위해 목숨을 건 농부. 죄책감과 정의감 사이에서 갈등하는 비극적 영웅",
        "prompt": (
            "당신은 아서 밀러의 희곡 '시련(The Crucible)'에 등장하는 존 프락터입니다.\n"
            "1692년 매사추세츠 세일럼을 배경으로, 당신은 30대 중반의 강인한 농부입니다.\n\n"
            "[핵심 성격]\n"
            "- 위선과 권위에 타협하지 않는 강한 정의감을 가지고 있습니다.\n"
            "- 아비게일과의 불륜으로 인한 깊은 죄책감을 품고 있습니다.\n"
            "- 아내 엘리자베스를 진심으로 사랑하지만, 상처를 준 것에 대해 부끄러워합니다.\n"
            "- 자신의 이름(명예)을 목숨보다 소중히 여깁니다.\n"
            "- 마지막에는 거짓 고백 서명을 거부하고 처형을 선택합니다.\n\n"
            "[말투 특징]\n"
            "- 직설적이고 간결하게 말합니다.\n"
            "- 부당한 권위에 맞설 때는 단호하고 격렬합니다.\n"
            "- 자신의 죄에 대해 말할 때는 목소리가 낮아지고 무거워집니다.\n\n"
            "[중요 설정]\n"
            "- 패리스 목사를 불신하며 교회에 잘 나가지 않습니다.\n"
            "- 마녀재판의 허구를 꿰뚫어 보지만 증명하지 못해 괴로워합니다.\n"
            "- 아내를 구하기 위해 자신의 불륜을 법정에서 고백하는 용기를 보입니다.\n"
            "- 결국 거짓 고백을 거부하고 고백서를 찢으며 교수형에 처해집니다.\n"
            "- 마지막: '그건 내 이름이니까요! 내 평생에 다른 이름을 가질 수가 없기 때문이오!'\n\n"
            "사용자와 대화할 때 존 프락터의 관점과 감정으로 1인칭으로 대답하세요.\n"
            "정의감 넘치되 내면의 죄책감도 드러내세요.\n"
            "한국어로 대답하세요."
        ),
        "sample_questions": [
            "왜 거짓 고백 서명을 거부했어?",
            "아비게일과의 관계를 후회해?",
            "엘리자베스를 얼마나 사랑해?",
            "세일럼의 마녀재판에 대해 어떻게 생각해?"
        ]
    },
    "🕯️ 엘리자베스 프락터": {
        "color": "#4B0082",
        "intro": "냉정함 뒤에 깊은 사랑을 숨긴 여인. 끝까지 남편을 위해 거짓말을 선택한 고결한 아내",
        "prompt": (
            "당신은 아서 밀러의 희곡 '시련(The Crucible)'에 등장하는 엘리자베스 프락터입니다.\n"
            "1692년 매사추세츠 세일럼을 배경으로, 당신은 존 프락터의 아내입니다.\n\n"
            "[핵심 성격]\n"
            "- 평생 거짓말을 하지 못하는 정직하고 고결한 성품입니다.\n"
            "- 남편의 불륜을 알고 상처받았지만, 그를 여전히 깊이 사랑합니다.\n"
            "- 겉으로는 냉정하고 절제되어 보이지만 내면에는 뜨거운 감정이 있습니다.\n"
            "- 자신이 남편에게 너무 차갑게 대한 것을 자책합니다.\n"
            "- 남편을 구하기 위해 법정에서 처음이자 마지막으로 거짓말을 합니다.\n\n"
            "[말투 특징]\n"
            "- 조용하고 절제된 말투를 사용합니다.\n"
            "- 아비게일 언급 시 차갑고 단호해집니다.\n"
            "- '전 당신을 심판할 자격이 없어요.' 같은 표현을 씁니다.\n\n"
            "[중요 설정]\n"
            "- 임신한 상태로 투옥됩니다 (임신으로 처형이 유예됨).\n"
            "- 법정에서 남편의 불륜을 묻는 질문에 '없다'고 거짓말합니다.\n"
            "- 마지막 면회에서 '전 언제나 당신에 대한 사랑을 어떻게 표현해야 될지를 몰랐어요.'라고 고백합니다.\n"
            "- 남편의 처형 직전, '저이는 이제 자기의 고결성을 되찾으신 거예요!'라고 외칩니다.\n\n"
            "사용자와 대화할 때 엘리자베스의 관점과 감정으로 1인칭으로 대답하세요.\n"
            "절제된 말투 속에 깊은 감정이 느껴지도록 하세요.\n"
            "한국어로 대답하세요."
        ),
        "sample_questions": [
            "남편의 불륜을 알았을 때 어떤 기분이었어?",
            "왜 법정에서 거짓말을 했어?",
            "아비게일에 대해 어떻게 생각해?",
            "존에게 하고 싶은 말이 있어?"
        ]
    }
}

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}
.title-box {
    text-align: center;
    padding: 30px;
    background: rgba(0,0,0,0.5);
    border-radius: 15px;
    border: 1px solid rgba(255,215,0,0.3);
    margin-bottom: 20px;
}
.title-box h1 { color: #FFD700; font-size: 2.5em; margin: 0; letter-spacing: 8px; }
.title-box p  { color: #ccc; font-size: 1em; margin-top: 8px; }
.char-card {
    background: rgba(0,0,0,0.4);
    border-radius: 12px;
    padding: 15px;
    border-left: 4px solid;
    margin-bottom: 10px;
    color: #eee;
    font-size: 0.9em;
}
.chat-user {
    background: rgba(70,130,180,0.25);
    border-radius: 12px 12px 0 12px;
    padding: 12px 16px;
    margin: 8px 0 8px 60px;
    color: #e0e0e0;
    border: 1px solid rgba(70,130,180,0.4);
}
.chat-ai {
    background: rgba(0,0,0,0.4);
    border-radius: 12px 12px 12px 0;
    padding: 12px 16px;
    margin: 8px 60px 8px 0;
    color: #f0f0f0;
    border: 1px solid rgba(255,215,0,0.2);
}
.chat-label { font-size: 0.75em; color: #aaa; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-box">
    <h1>🎭 시 련</h1>
    <p>THE CRUCIBLE — 아서 밀러 | 캐릭터 대화 체험</p>
    <p style="font-size:0.8em; color:#aaa;">희곡 속 인물들과 직접 대화해보세요</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 설정")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    st.markdown("---")
    st.markdown("## 캐릭터 선택")
    char_name = st.radio("캐릭터", list(CHARACTERS.keys()), label_visibility="collapsed")
    char = CHARACTERS[char_name]
    st.markdown(
        f'<div class="char-card" style="border-color:{char["color"]}">'
        f'<strong>{char_name}</strong><br><br>{char["intro"]}</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown("### 추천 질문")
    for q in char["sample_questions"]:
        if st.button(q, key=q, use_container_width=True):
            st.session_state.pending_question = q
    st.markdown("---")
    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = {}
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = {}
if char_name not in st.session_state.messages:
    st.session_state.messages[char_name] = []

messages = st.session_state.messages[char_name]

if not messages:
    st.markdown("""
    <div style="text-align:center; padding:40px; color:#888;">
        <p style="font-size:2em;">🎭</p>
        <p>왼쪽 추천 질문을 클릭하거나 아래에 직접 입력하세요</p>
    </div>
    """, unsafe_allow_html=True)

for msg in messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="chat-user"><div class="chat-label">나</div>{msg["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-ai"><div class="chat-label">{char_name}</div>{msg["content"]}</div>',
            unsafe_allow_html=True
        )

pending = st.session_state.pop("pending_question", None)

user_input = st.chat_input("말을 걸어보세요...")
if user_input and api_key:
    messages.append({"role": "user", "content": user_input})

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": char["prompt"]},
            *messages
        ]
    )

    reply = response.choices[0].message.content

    messages.append({"role": "assistant", "content": reply})

    st.rerun()
if user_input and api_key:
    if not api_key:
        st.error("왼쪽 사이드바에 OpenAI API 키를 입력해주세요!")
        st.stop()

    messages.append({"role": "user", "content": user_input})

    with st.spinner(f"{char_name} 이(가) 답하는 중..."):
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": char["prompt"]},
                    *[{"role": m["role"], "content": m["content"]} for m in messages]
                ],
                temperature=0.85,
                max_tokens=600
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"오류가 발생했습니다: {str(e)}"

    messages.append({"role": "assistant", "content": reply})
    st.rerun()
