import streamlit as st
import pandas as pd
import datetime

st.set_page_config(layout="wide")
# 시간표 데이터 생성 (7교시까지 포함)
timetables = {
    '1학년': {
        '2반': {
            '교시': ['1', '2', '3', '4', '5', '6', '7'],
            '월요일': ['통사', '영어', '정보', '국어', '수학', '미술', '통과'],
            '화요일': ['통사', '체육', '국어', '수학', '영어', '', '창체'],
            '수요일': ['미술', '실험', '통과', '체육', '영어', '음악', '국어'],
            '목요일': ['통과', '국어', '음악', '수학', '통사', '진직', '영어'],
            '금요일': ['수학', '정보', '통과', '통사', '독교', '창체', '창체']
        },
        # ... 더 많은 반 데이터 추가
    },
}

# Streamlit 앱 제목 설정
col1, col2 = st.columns([1, 0.4])
with col1:
    st.title("경혜여자고등학교 시간표")
with col2:
    st.image("경혜여자고등학교 로고.png", width=200, use_column_width=False)


# 학년과 반 선택 상자를 한 줄에 배치
col1, col2 = st.columns(2)
with col1:
    grade = st.selectbox("학년 선택", list(timetables.keys()))
with col2:
    classroom = st.selectbox("반 선택", list(timetables[grade].keys()))

# 선택된 학년과 반의 시간표 데이터프레임 생성
timetable = timetables[grade][classroom]
df = pd.DataFrame(timetable)
df.set_index('교시', inplace=True)

# 오늘 요일 감지
today = datetime.datetime.today().strftime('%A')
# 요일을 한국어로 변환
days_english_to_korean = {
    'Monday': '월요일',
    'Tuesday': '화요일',
    'Wednesday': '수요일',
    'Thursday': '목요일',
    'Friday': '금요일',
    'Saturday': '토요일',
    'Sunday': '일요일'
}
today_korean = days_english_to_korean[today]

# 요일에 맞는 열 색상 적용 함수
def highlight_today(col):
    if col.name == today_korean:
        return ['background-color: #ffeb3b; color: black'] * len(col)
    else:
        return [''] * len(col)

# HTML/CSS 스타일링 추가
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f0f2f6;
    }
    .dark-mode .reportview-container {
        background: #2e2e2e;
    }
    .dataframe table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        font-size: 20px; /* 폰트 크기 증가 */
    }
    .dataframe th, .dataframe td {
        border: 1px solid #dddddd;
        text-align: center;
        padding: 12px; /* 패딩 증가 */
    }
    .dataframe th {
        background-color: #4CAF50;
        color: white;
    }
    .dark-mode .dataframe th {
        background-color: #1a1a1a;
        color: #f0f0f0;
    }
    .dataframe td {
        background-color: #ffffff;
        color: black;
    }
    .dark-mode .dataframe td {
        background-color: #333333;
        color: #f0f0f0;
    }
    .dataframe tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    .dark-mode .dataframe tr:nth-child(even) {
        background-color: #2a2a2a;
    }
    </style>
    <script>
    const observer = new MutationObserver((mutations) => {
        const darkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        if (darkMode) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    });
    observer.observe(document.body, { attributes: true, childList: true, subtree
    });
    </script>
    """,
    unsafe_allow_html=True
)

# 시간표 출력
st.write(f"{grade} {classroom}")
st.dataframe(df.style.apply(highlight_today, axis=0).set_properties(**{
    'border': '1px solid black',
    'font-size': '20px',  # 폰트 크기 증가
    'text-align': 'center'
}).set_table_styles([{
    'selector': 'th',
    'props': [('font-size', '22px')]  # 헤더 폰트 크기 증가
}]), width=1920)
