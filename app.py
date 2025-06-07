from flask import Flask, render_template, request

app = Flask(__name__)

# 고등학교 유형별 추천 기준 (가중치 적용)
def recommend_school(responses):
    scores = {
        '자율형사립고': 0,
        '일반고': 0,
        '국제고': 0,
        '예술·체육고': 0,
        '특성화고': 0,
        '과학고': 0,
        '외국어고': 0
    }

    # Q1~Q2: 특정 과목에 대한 흥미와 자신감
    academic_subjects = ['q1_korean', 'q1_english', 'q1_math', 'q1_science', 'q1_social']
    science_subjects = ['q1_math', 'q1_science']
    arts_subjects = ['q1_music', 'q1_art', 'q1_pe']
    tech_subjects = ['q1_tech', 'q1_computer']
    language_subjects = ['q1_english', 'q1_second']

    # 자율형사립고: 학업 중심 과목 평균
    scores['자율형사립고'] += sum(int(responses[q]) for q in academic_subjects) / len(academic_subjects) * 2

    # 일반고: 모든 과목 평균
    scores['일반고'] += sum(int(responses[q]) for q in responses.keys() if q.startswith('q1_')) / len(responses.keys())

    # 과학고: 수학, 과학 점수
    scores['과학고'] += sum(int(responses[q]) for q in science_subjects) / len(science_subjects) * 2

    # 예술·체육고: 예체능 과목 점수
    scores['예술·체육고'] += sum(int(responses[q]) for q in arts_subjects) / len(arts_subjects) * 2

    # 특성화고: 기술·가정, 컴퓨터 관련 점수
    scores['특성화고'] += sum(int(responses[q]) for q in tech_subjects) / len(tech_subjects) * 2

    # 외국어고: 영어 및 제2외국어 점수
    scores['외국어고'] += sum(int(responses[q]) for q in language_subjects) / len(language_subjects) * 2

    # 국제고: 외국어 및 글로벌 가치 점수
    scores['국제고'] += int(responses['q5_global']) * 2

    # 가장 높은 점수를 가진 고등학교 유형 선택
    recommended_school = max(scores, key=scores.get)

    return recommended_school

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        responses = request.form.to_dict()
        recommended_school = recommend_school(responses)  # 추천 알고리즘 실행
        return render_template('result.html', responses=responses, recommended_school=recommended_school)
    return render_template('survey.html')

if __name__ == '__main__':
    app.run(debug=True)