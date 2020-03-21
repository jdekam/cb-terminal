<template>
  <section class="section is-clipped">
   <div class="tile is-ancestor">
      <div class="tile is-vertical is-parent is-7">
        <div class="tile is-child cb-welcome">
          <div class="card is-vertical-centered">
            <div class="card-image is-pulled-left">
              <figure class="image is-square">
                <img src="../assets/chezbetty_1000px.jpg">
              </figure>
            </div>
            <div class="card-content">
              <p class="title">
                Welcome to Chez Betty!
              </p>
              <p class="subtitle">
                We are a student operated food coop that sells affordably priced snacks and beverages.
                Not sure what to do? Take a look at the posters immediately behind you!
              </p>
            </div>
          </div>
        </div>
        <div class="tile is-child">
          <div class="card is-vertical-centered">
            <div class="card-content">
              <div class="notification is-info is-size-4" v-for="announcement in announcements" :key="announcement.id">
                {{ announcement.content }}
              </div>
            </div>
          </div>
        </div>
        <div class="tile is-child cb-translate">
          <div class="card is-vertical-centered">
            <div class="card-content">
              <div class="buttons is-centered">
                <button class="button">English</button>
                <button class="button">Deutsch</button>
                <button class="button">français</button>
                <button class="button">漢語</button>
                <button class="button">简体中文</button>
                <button class="button">فارسی</button>
                <button class="button">Română</button>
                <button class="button">Español</button>
                <button class="button">العربية</button>
              </div>
              <p class="subtitle">
                Can you help translate Betty? Check us out on Github!
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="tile is-vertical is-parent is-5">
        <div class="tile is-child cb-debt">
           <div class="card is-vertical-centered">
            <div class="card-content">
                <p class="title">
                  Current Chez Betty Debt: <span class="has-text-danger">${{ debt }}</span>
                </p>
                <p class="subtitle">
                  We depend on you to pay off your debts in a timely manner!
                </p>
            </div>
          </div>
        </div>
        <div class="tile is-child">
          <div class="card">
            <div class="card-header">
              <p class="card-header-title is-centered is-size-3">
                Swipe your M-Card or Enter your UMID
              </p>
            </div>
            <div class="card-content cb-kp-container">
              <div class="cb-kp-progress">
                <progress class="progress is-medium is-info" value="0" max="8">45%</progress>
              </div>
              <div class="field is-grouped is-fullwidth cb-kp-buttons">
                <button class="button" v-for="i in 3" :key="i" @click="handleKeypadEntry(i + 0)">{{ i + 0 }}</button>
              </div>
              <div class="field is-grouped is-fullwidth cb-kp-buttons">
                <button class="button" v-for="i in 3" :key="i" @click="handleKeypadEntry(i + 3)">{{ i + 3 }}</button>
              </div>
              <div class="field is-grouped is-fullwidth cb-kp-buttons">
                <button class="button" v-for="i in 3" :key="i" @click="handleKeypadEntry(i + 6)">{{ i + 6 }}</button>
              </div>
              <div class="field is-grouped is-fullwidth cb-kp-buttons">
                <button class="button" @click="handleKeypadEntry('Clear')">Clear</button>
                <button class="button" @click="handleKeypadEntry('Delete')">&laquo;</button>
                <button class="button" @click="handleKeypadEntry(0)">0</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="modal">
      <div class="modal-background" @click="toggleModal()"></div>
      <div class="modal-content">
        <div class="notification is-danger is-size-3">
          <span v-if="scanned">
            Your UMID scan was not recognized. Try swiping your M-Card again. If the issue persists, 
            please e-mail the Chez Betty development team at <a>chezbetty@umich.edu</a> so that 
            we can take a look.
          </span>
          <span v-else>
            Your UMID entry was not recognized. If this is your first time using Chez Betty you need to 
            create an account by swiping your M-Card at this kiosk. If you are sure you already have 
            a Betty account, try re-entering your UMID.
          </span>
        </div>
      </div>
      <button class="modal-close is-large" @click="toggleModal()"></button>
    </div>
  </section>
</template>

<style lang="scss">
  // helper to vertically center items
  .is-vertical-centered {
    display: flex;
    align-items: center;
  }

  // remove vertical scrollbar
  ::-webkit-scrollbar {
    display: none; 
  }

  // make page fill screen
  .section {
    background-color: #ECECEC;
    height: 100vh;
  }

  // make tiles fill page
  .is-ancestor {
    height: 100%;
    margin: 0 !important; // this Bulma class has some weird margins by default
  }

  // make cards fill tiles
  .card {
    height: 100%;

    .card-content {
      width: 100%;
    }
  }

  // style chez betty logo
  .card-image {
    padding: .75rem;

    figure {
      width: 20vh;
    }

    img {
      width: 100%;
      height: 100%;
    }
  }

  // fix height of welcome card
  .cb-welcome {
    max-height: 20vh;
  }

  // fix height of translate / debt cards
  .cb-translate, .cb-debt {
    max-height: 10vh;
  }

  // keypad css rules
  .cb-kp-container {
    display: flex;
    flex-direction: column;

    .cb-kp-progress {
      margin-bottom: 1rem;
    }

    .cb-kp-buttons {
      flex: 3;

      button {
        font-size: 2.5rem;
      }
    }

    button {
      width: 100%;
      height: 100%;
    }

    button:not(:last-child) {
      margin-right: .75rem;
    }
  }
</style>

<script>
export default {
  data() {
    return {
      umid: '',
      scanned: null,
      debt: '3,129.29',
      announcements: [
        {
          content: "Remember, you save 5% if you keep $20 or more in your account.",
        },
        {
          content: "Help us restock! But please, don't put boxes where they don't go."
        },
        {
          content: "Chez Betty is in a critical amount of debt at the moment. If items are currently unstocked, it is because we are unable to buy new items until the debt is under $2000."
        },
      ],
    }
  },
  // this hook runs when page is being loaded
  created: function () {
    // this.getAnnouncements();
    // this.getDebt();
  },
  // this hook runs after page has been rendered
  mounted: function () {
    // get height of keypad header
    const header_height = document.querySelector('.card-header').clientHeight
    // dynamically set height of keypad
    const keypad_height = `calc(100% - ${header_height}px)`
    document.querySelector('.cb-kp-container').style.height = keypad_height
  },
  methods: {
    /**
     * AJAX requests
     */
    getAnnouncements() {
      const url = '/terminal_get_announcements/'
      this.$axios.get(url).then(result => {
        this.announcements = result.data
      })
      .catch(error => {
        console.log(error)
      })
    },
    getDebt() {
      const url = '/terminal_get_debt/'
      this.$axios.get(url).then(result => {
        this.debt = result.data.debt
      })
      .catch(error => {
        console.log(error)
      })
    },
    checkUmid() {
      const url = '/terminal_check_umid/'
      this.$axios.post(url, {
        umid: this.umid,
        scanned: this.scanned,
      })
      .then((response) => {
        this.$router.push({ name: 'terminal', params: { umid: response.data.umid }})
      })
      .catch((error) => {
        console.log(error)
        this.toggleModal();
      })
    },
    /**
     * Keypad toggles / click handlers
     */
    toggleModal() {
      const modal = document.querySelector('.modal')
      if (modal.classList.contains('is-active')) {
        modal.classList.remove('is-active')
      } else {
        // clear umid data and reset progress bar
        this.scanned = null
        this.umid = ''
        document.querySelector('.progress').setAttribute('value', this.umid.length)
        modal.classList.add('is-active')
      }
    },
    handleKeypadEntry(key) {
      if (Number.isInteger(key)) {
        this.umid += key
        if (this.umid.length === 8) {
          document.querySelector('.progress').removeAttribute('value')
          this.checkUmid()
          return;
        }
      } else {
        if (key === 'Clear') {
          this.umid = ''
        }
        else if (key === 'Delete') {
          this.umid = this.umid.slice(0, -1);
        }
      }
      document.querySelector('.progress').setAttribute('value', this.umid.length)
    }
  }
}
</script>