<template>
  <div class="row">
    <div class="col-md-7">
      <!-- USER DEBT -->
      <div class="row">
        <div class="col-md-12">
          <h1 style="font-size:375%;">
          <img src="../assets/chezbetty_1000px.jpg" style="margin-top: 5px; width: 180px;">
          Current User Debt: <strong>{{ debt }}</strong>
          </h1>
        </div>
      </div>

      <!-- ANNOUNCEMENTS -->
      <div class="row">
        <div class="col-md-12">
          <div id="announcements" style="font-size:20pt;">
            <div 
              class="alert alert-info" role="alert"
              v-for="announcement in announcements"
              :key="announcement.id"
            >
              {{ announcement.content }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="col-md-5" style="text-align: center;">
      <!-- DIRECTIONS -->
      <div style="margin-top:100px;">
        <h2>Swipe your M-Card to login</h2>
      </div>
      <hr>
      <div class="or"><span>OR</span></div>
      <div class="center">
        <h2>Enter your UMID here</h2>
      </div>
    </div>
  </div>
</template>

<style scoped>
  body {
    padding-bottom: 100px;
  }

  .keypad-lg container {
    width: 480px;
    display: inline-block;
  }

  .keypad-lg block {
    width: 150px;
    height: 150px;
    margin: 5px;
    float: right;
  }

  block[v2] {
    height: 210px;
  }

  block[h2] {
    width: 210px;
  }

  block[h3] {
    width: 320px;
  }

  .keypad-lg .btn-keypad {
    height: 150px;
    width: 150px;
    font-size: 22pt;
  }

  .keypad-lg .btn-keypad-wide {
    height: 150px;
    width: 310px;
    font-size: 14pt;
  }

  .keypad-lg .btn-keypad-triplewide {
    height: 150px;
    width: 470px;
    font-size: 14pt;
  }

  .keypad-lg .btn-full-width {
    width: 470px;
    height: 150px;
    margin: 0 5px;
  }

  .keypad-lg .keypad-full-width {
    width: 480px;
    margin: 5px;
  }

  .keypad-sm container {
    width: 330px;
    display: inline-block;
  }

  .keypad-sm block {
    margin: 5px;
    float: right;
  }

  .keypad-sm .btn-keypad {
    height: 100px;
    width: 100px;
    font-size: 14pt;
  }

  .keypad-sm .btn-keypad-wide {
    height: 100px;
    width: 110px;
    font-size: 14pt;
  }

  .keypad-sm .btn-keypad-triplewide {
    height: 100px;
    width: 330px;
    font-size: 14pt;
  }

  .keypad-sm .btn-full-width {
    width: 330px;
    height: 100px;
    margin: 0 5px;
  }

  .keypad-sm .keypad-full-width {
    width: 330px;
    margin: 5px;
  }

  #keypad-umid-status .umid-status-block {
    width: 54px;
    height: 54px;
    margin-right: 3px;
    margin-left: 3px;
  }

  .umid-status-blue {
    background-color: #428bca;
  }
</style>

<script>
import 'jquery'
import 'bootstrap'
import axios from 'axios'

export default {
  data() {
    return {
      debt: 'Loading',
      umid: '',
      scanned: false,
      announcements: [
        {
          content: "Placeholder announcement!",
        },
      ],
    }
  },
  methods: {
    getAnnouncements() {
      const url = '/terminal_get_announcements/'
      axios.get(url).then(result => {
        this.announcements = result.data
      })
      .catch(error => {
        console.log(error)
      })
    },
    getDebt() {
      const url = '/terminal_get_debt/'
      axios.get(url).then(result => {
        this.debt = result.data.debt
      })
      .catch(error => {
        console.log(error)
      })
    },
    checkUmid() {
      const url = '/terminal_check_umid/'
      axios.post(url, {
        umid: this.umid,
        scanned: this.scanned,
      })
      .then((response) => {
        this.$router.push({ name: 'terminal', params: { umid: response.data.umid }})
      })
      .catch((error) => {
        console.log(error)
        // snackbar error message, clear keypad
      })
    },
  }
}
</script>