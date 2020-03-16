<template>
  <section class="section">
    <div class="columns">
      <div class="column is-three-fifths">
        <section class="section has-text-justified">
          <img class="cb-icon" src="../assets/chezbetty_1000px.jpg">
          <span class="cb-title is-size-1">
            Current User Debt:&nbsp;
            <span class="has-text-weight-bold has-text-danger">
              {{ debt }}
            </span>
          </span>
        </section>
        <section class="section">
          <article 
            class="message is-info"
            v-for="announcement in announcements"
            :key="announcement.index"
          >
            <div class="message-body is-size-3">
              {{ announcement.content }}
            </div>
          </article>
        </section>
      </div>
      <div class="column">
        <section class="section has-text-centered">
          <p class="is-size-2 has-text-align">
            Swipe your M-Card to login
          </p>
          <p class="is-size-4">
            OR
          </p>
          <p class="is-size-2">
            Enter your UMID below
          </p>
          <!-- Indicators -->
          <div class="columns">
            <div class="column">
              <button class="button cb-indicator"></button>
            </div>
            <div class="column">
              <button class="button cb-indicator"></button>
            </div>
            <div class="column">
              <button class="button cb-indicator"></button>
            </div>
            <div class="column">
              <button class="button cb-indicator"></button>
            </div>
            <div class="column">
              <button class="button cb-indicator"></button>
            </div>
            <div class="column">
              <button class="button cb-indicator"></button>
            </div>
            <div class="column">
              <button class="button cb-indicator"></button>
            </div>
            <div class="column">
              <button class="button cb-indicator"></button>
            </div>
          </div>
          <!-- Keypad -->
          <div class="columns">
             <div class="column">
              <button class="button is-fullwidth">1</button>
            </div>
            <div class="column">
              <button class="button is-fullwidth">2</button>
            </div>
            <div class="column">
              <button class="button is-fullwidth">3</button>
            </div>
          </div>
          <div class="columns">
             <div class="column">
              <button class="button is-fullwidth">4</button>
            </div>
            <div class="column">
              <button class="button is-fullwidth">5</button>
            </div>
            <div class="column">
              <button class="button is-fullwidth">6</button>
            </div>
          </div>
          <div class="columns">
             <div class="column">
              <button class="button">7</button>
            </div>
            <div class="column">
              <button class="button">8</button>
            </div>
            <div class="column">
              <button class="button">9</button>
            </div>
          </div>
          <div class="columns">
             <div class="column">
              <button class="button">0</button>
            </div>
            <div class="column">
              <button class="button">&lt;</button>
            </div>
            <div class="column">
              <button class="button">Clear</button>
            </div>
          </div>
        </section>
      </div>
    </div>
  </section>
</template>

<style scoped>
  .cb-icon {
    width: 180px;
    height: 180px;
    vertical-align: middle;
    margin-right: 1em;
  }
  .cb-title {
    vertical-align: middle;
  }
  .cb-umid-indicator {
    pointer-events: none;
  }
  .cb-umid-buttons {
    display: flex;
    flex-flow: column;
  }
</style>

<script>
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