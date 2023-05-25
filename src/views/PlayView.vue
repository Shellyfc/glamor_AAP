<template>
	<main class="app">
		<h1>The Quiz</h1>

		<section class="quiz" v-if="!quizCompleted">
			<div v-if="getCurrentQuestion && questions">
				<div class="quiz-info">
					<span class="question">{{ questionIdx + 1 }}. {{ getCurrentQuestion.question }}</span>
					<span class="score">Score {{ score }}/{{ questions.length }}</span>
				</div>

				<div class="input_answer">
					<q-input outlined v-model="answer" />
				</div>
				<button @click="NextQuestion" :disabled="!answer">
					{{
						getCurrentQuestion.index == questions.length - 1
						? 'Finish'
						: answer
							? 'Submit'
							: 'Next question'
					}}
				</button>
			</div>

		</section>

		<section v-else>
			<h2>You have finished the quiz!</h2>
			<p>Your score is {{ score }}/{{ questions.length }}</p>
			<div>
				Question: {{ questions[page - 1].question }}
				Your Answer: {{ questions[page - 1].userAnswer }}
				<li v-for="(ta, index) in questions[page - 1].topAnswer" :key="index">
					{{ ta[3] }} Vote: {{ ta[5] }}
				</li>
			</div>
			<div class="q-pa-lg flex flex-center">
				<q-pagination v-model="page" :max="questions.length" direction-links push color="teal" active-design="push"
					active-color="orange" />
			</div>
		</section>
	</main>
</template>

<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios'
import { getAuth } from "firebase/auth";
// import { get } from 'http';
const answer = ref('')
// const url = ref('http://192.168.1.23')
// const url = ref('http://10.26.27.216')
// const url = ref('http://10.25.226.91')
const url = ref('http://127.0.0.1')
const questions = ref(null)
const quizCompleted = ref(false)
const questionIdx = ref(0)
const email = ref(null)
const page = ref(1)
getAuth().onAuthStateChanged(function (user) {
	if (user) {
		email.value = user.email
	} else {
		email.value = ""
	}
})
const score = computed(() => {
	let value = 0
	if (questions.value) {
		questions.value.map(q => {
			if (q.userAnswer != null && q.answer == q.userAnswer) {
				// console.log('correct');
				value++
			}
		})
	}

	return value
})


function getQuestions() {
	let axiosConfig = {
		headers: {
			'Content-Type': 'application/json;charset=UTF-8',
			"Access-Control-Allow-Origin": "*",
		}
	};
	axios.post(url.value + ":8888/play/questions", {
		num: 5
	}, axiosConfig)
		.then(function (response) {
			questions.value = response.data
		})
		.catch(function (error) {
			console.log(error);
		});
}

onBeforeMount(() => {
	getQuestions()
})

const getCurrentQuestion = computed(() => {
	if (questions.value) {
		let question = questions.value[questionIdx.value]
		console.log(questions.value)
		question.index = questionIdx.value
		return question
	}
	return false
})
// const SetAnswer = (e) => {
// 	questions.value[currentQuestion.value].userAnswer = e
// 	console.log(e.value)
//     console.log(currentQuestion)
//     console.log(questions.value[currentQuestion.value])
//     return
// }

const NextQuestion = () => {
	questions.value[questionIdx.value].userAnswer = answer.value
	answer.value = ''
	if (questionIdx.value < questions.value.length - 1) {
		let axiosConfig = {
			headers: {
				'Content-Type': 'application/json;charset=UTF-8',
				"Access-Control-Allow-Origin": "*",
			}
		};
		axios.post(url.value + ":8888/play/answer", {
			email: email.value,
			question: questions.value[questionIdx.value],
			answer: questions.value[questionIdx.value].userAnswer
		}, axiosConfig)
			.then(function (response) {
				console.log(response);
				questions.value[questionIdx.value].topAnswer = response.data;
			})
			.catch(function (error) {
				console.log(error);
			});
		questionIdx.value++
		return
	}
	quizCompleted.value = true;
}
</script>

<style scoped>
* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
	font-family: 'Montserrat', sans-serif;
}

body {
	background-color: #271c36;
	color: #FFF;
}

.app {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 2rem;
	height: 100vh;
}

h1 {
	font-size: 2rem;
	margin-bottom: 2rem;
}

.quiz {
	/* background-color: #382a4b; */
	padding: 1rem;
	width: 100%;
	max-width: 640px;
}

.quiz-info {
	display: flex;
	justify-content: space-between;
	margin-bottom: 1rem;
}

.quiz-info .question {
	/* color: #8F8F8F; */
	font-size: 1.25rem;
}

.quiz-info .score {
	/* color: #FFF; */
	font-size: 1.25rem;
}

.options {
	margin-bottom: 1rem;
}

.input_answer {
	margin-bottom: 1rem;
}

.option {
	padding: 1rem;
	display: block;
	background-color: #271c36;
	margin-bottom: 0.5rem;
	border-radius: 0.5rem;
	cursor: pointer;
}

.option:hover {
	background-color: #2d213f;
}

.option.correct {
	background-color: #2cce7d;
}

.option.wrong {
	background-color: #ff5a5f;
}

.option:last-of-type {
	margin-bottom: 0;
}

.option.disabled {
	opacity: 0.5;
}

.option input {
	display: none;
}

button {
	appearance: none;
	outline: none;
	border: none;
	cursor: pointer;
	padding: 0.5rem 1rem;
	background-color: #2cce7d;
	color: #2d213f;
	font-weight: 700;
	text-transform: uppercase;
	font-size: 1.2rem;
	border-radius: 0.5rem;
}

button:disabled {
	opacity: 0.5;
}

h2 {
	font-size: 2rem;
	margin-bottom: 2rem;
	text-align: center;
}

p {
	color: #8F8F8F;
	font-size: 1.5rem;
	text-align: center;
}
</style>