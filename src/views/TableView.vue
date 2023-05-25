<template>
  <div class="q-pa-md">

    <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
      <div class="q-gutter-md row items-start flex flex-center">
        <q-input filled v-model="formA" label="Your choice of A" hint="A" lazy-rules
          :rules="[val => val && val.length > 0 || 'Please type something']" />

        <q-input filled v-model="formB" label="Your choice of B" hint="B" lazy-rules
          :rules="[val => val && val.length > 0 || 'Please type something']" />

        <q-input filled v-model="formC" label="Your choice of C" hint="C" lazy-rules
          :rules="[val => val && val.length > 0 || 'Please type something']" />

        <q-input filled v-model="formD" label="Your choice of D" hint="D" lazy-rules
          :rules="[val => val && val.length > 0 || 'Please type something']" />
      </div>
      <div>
        <q-btn label="Submit" type="submit" color="primary" />
        <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
      </div>

    </q-form>

  </div>

  <div class="q-pa-md flex flex-center" v-if="bIsLoading">
    <q-circular-progress indeterminate rounded size="50px" color="light-blue" class="q-ma-md" />
  </div>

  <div class="q-pa-md" v-if="rowsB">
    <q-table title="Model Predictions for B" :rows="rowsB" :columns="columnsB" row-key="name" />
  </div>
  <div class="q-pa-md" v-if="rowsD">
    <q-table title="Model Predictions for D" :rows="rowsD" :columns="columnsD" row-key="name" />
  </div>


  <div v-if="(bAskingQuestions && questions)">
    <div class="q-pa-md">
      {{ questions[questionIdx]["question"] }}
      <div class="q-pa-md flex flex-center">
        <q-input style="max-width: 150px" v-model="answer" label="Your answer" />
      </div>
      <div class="q-pa-md q-gutter-sm">
        <!-- <q-btn label="Submit" @click="submitAnswer()" color="primary" /> -->
        <q-btn label="Next" @click="nextExample()" color="primary" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useQuasar } from 'quasar'
import { getAuth } from "firebase/auth";

export default {
  setup() {
    const answer = ref(null)

    const questions = ref(null)

    const formA = ref(null)
    const formB = ref(null)
    const formC = ref(null)
    const formD = ref(null)
    const columnsB = [
      {
        name: 'model',
        required: true,
        label: 'model',
        align: 'left',
        field: 'model',
        sortable: true
      },
      { name: 'top', align: 'center', label: 'top', field: 'top', sortable: true },
      { name: 'topScore', label: 'topScore', field: 'topScore', sortable: true },
      { name: 'topRank', label: 'topRank', field: 'topRank', sortable: true },
      { name: 'topSentence', label: 'topSentence', field: 'topSentence' },
      { name: 'answer', label: 'answer', field: 'answer' },
      { name: 'answerScore', label: 'answerScore', field: 'answerScore', sortable: true },
      { name: 'answerRank', label: 'answerRank', field: 'answerRank', sortable: true },
      { name: 'answerSentence', label: 'answerSentence', field: 'answerSentence' }
    ]
    const columnsD = [
      {
        name: 'model',
        required: true,
        label: 'model',
        align: 'left',
        field: 'model',
        sortable: true
      },
      { name: 'top', align: 'center', label: 'top', field: 'top', sortable: true },
      { name: 'topScore', label: 'topScore', field: 'topScore', sortable: true },
      { name: 'topRank', label: 'topRank', field: 'topRank', sortable: true },
      { name: 'topSentence', label: 'topSentence', field: 'topSentence' },
      { name: 'answer', label: 'answer', field: 'answer' },
      { name: 'answerScore', label: 'answerScore', field: 'answerScore', sortable: true },
      { name: 'answerRank', label: 'answerRank', field: 'answerRank', sortable: true },
      { name: 'answerSentence', label: 'answerSentence', field: 'answerSentence' }
    ]
    const rowsB = ref(null)
    const rowsD = ref(null)
    const bIsLoading = ref(false)
    const bAskingQuestions = ref(true)

    const qq = useQuasar()

    const email = ref(null)
    getAuth().onAuthStateChanged(function (user) {
      if (user) {
        email.value = user.email
      } else {
        email.value = ""
      }
    })

    const questionIdx = ref(0)
    // const url = ref('http://10.26.27.216')
    // const url = ref('http://10.25.226.91')
    // const url = ref('http://192.168.1.23')
    const url = ref('http://127.0.0.1')

    function queryQuestions() {
      let axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          "Access-Control-Allow-Origin": "*",
        }
      };
      axios.post(url.value + ":8888/table/questions", {
        num: 10
      }, axiosConfig)
        .then(function (response) {
          console.log(response);
          questions.value = response.data
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    onMounted(() => {
      queryQuestions()
    })

    return {
      formA,
      formB,
      formC,
      formD,
      columnsB,
      rowsB,
      columnsD,
      rowsD,
      qq,
      email,
      bIsLoading,
      bAskingQuestions,
      questions,
      questionIdx,
      queryQuestions,
      answer,

      onSubmit() {
        // qq.loading.show({
        //   spinner: QSpinnerInfinity,
        //   message: 'Fetching data. Hang on...',
        // });
        rowsB.value = null;
        rowsD.value = null;
        bIsLoading.value = true;
        bAskingQuestions.value = true;
        let axiosConfig = {
          headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            "Access-Control-Allow-Origin": "*",
          }
        };
        axios.post(url.value + ":8888/table/queryOnlineResult", {
          email: email.value,
          formA: formA.value,
          formB: formB.value,
          formC: formC.value,
          formD: formD.value,
        }, axiosConfig)
          .then(function (response) {
            // qq.loading.hide()
            bIsLoading.value = false
            console.log(response);
            rowsB.value = response.data["B"]
            rowsD.value = response.data["D"]
          })
          .catch(function (error) {
            console.log(error);
            qq.loading.hide()
          });
      },

      onReset() {
        formA.value = null
        formB.value = null
        formC.value = null
        formD.value = null
        bIsLoading.value = false
        bAskingQuestions.value = false
      },

      submitAnswer() {
        let axiosConfig = {
          headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            "Access-Control-Allow-Origin": "*",
          }
        };
        axios.post(url.value + ":8888/table/answer", {
          email: email.value,
          question: questions.value[questionIdx.value],
          answer: answer.value
        }, axiosConfig)
          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
      },

      nextExample() {
        this.submitAnswer()
        if (questionIdx.value < questions.value.length) {
          questionIdx.value += 1;
          answer.value = null
        } else {
          this.queryExamples();
        }
      }
    }
  }
}
</script>