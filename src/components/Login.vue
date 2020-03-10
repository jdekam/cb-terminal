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
            class="message"
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
</style>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      debt: '$1.00',
      umid: '',
      scanned: false,
      announcements: [
        {
          content: "This is an announcement!",
        },
        {
          content: "Hello there! Repay your damn debt!",
        },
      ],
    }
  },
  methods: {
    getAnnouncements() {
      // api call to retreive announcements
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
    getDebt() {
      // api call to retreive user debt
    },
  }
}
</script>