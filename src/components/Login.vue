<template>
  <section class="section is-clipped">
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-parent is-7">
        <div class="tile is-child cb-welcome">
          <div class="card is-vertical-centered">
            <div class="card-image is-pulled-left">
              <figure class="image is-square">
                <img src="../assets/chezbetty_1000px.jpg" alt="Logo" />
              </figure>
            </div>
            <div class="card-content">
              <p class="title">Welcome to Chez Betty!</p>
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
              <div 
                class="notification is-info is-size-4" 
                v-for="(announcement, index) in announcements" 
                :key="index"
              >
                {{ announcement }}
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
              <p class="subtitle">Can you help translate Betty? Check us out on Github!</p>
            </div>
          </div>
        </div>
      </div>
      <div class="tile is-vertical is-parent is-5">
        <div class="tile is-child cb-debt">
          <div class="card is-vertical-centered">
            <div class="card-content">
              <p class="title">
                Current Chez Betty Debt:
                <span class="has-text-danger">${{ debt }}</span>
              </p>
              <p class="subtitle">We depend on you to pay off your debts in a timely manner!</p>
            </div>
          </div>
        </div>
        <div class="tile is-child">
          <div class="card">
            <div class="card-header">
              <p
                class="card-header-title is-centered is-size-3"
              >Swipe your M-Card or Enter your UMID</p>
            </div>
            <div class="card-content cb-kp-container">
              <div class="cb-kp-progress">
                <progress class="progress is-medium is-info" value="0" max="8">45%</progress>
              </div>
              <div class="field is-grouped is-fullwidth cb-kp-buttons">
                <button
                  class="button"
                  v-for="i in 3"
                  :key="i"
                  @click="handleKeypadEntry(i + 0)"
                >{{ i + 0 }}</button>
              </div>
              <div class="field is-grouped is-fullwidth cb-kp-buttons">
                <button
                  class="button"
                  v-for="i in 3"
                  :key="i"
                  @click="handleKeypadEntry(i + 3)"
                >{{ i + 3 }}</button>
              </div>
              <div class="field is-grouped is-fullwidth cb-kp-buttons">
                <button
                  class="button"
                  v-for="i in 3"
                  :key="i"
                  @click="handleKeypadEntry(i + 6)"
                >{{ i + 6 }}</button>
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
            please e-mail the Chez Betty development team at
            <a>chezbetty@umich.edu</a> so that
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

<style scoped lang="scss">
// helper to vertically center items
.is-vertical-centered {
  display: flex;
  align-items: center;
}

// remove vertical scrollbar
::-webkit-scrollbar {
  display: none;
}

// remove overflow scrollbars
html {
  overflow: hidden;
}

// make page fill screen
.section {
  background-color: #ececec;
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
  padding: 0.75rem;

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
.cb-translate,
.cb-debt {
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
    margin-right: 0.75rem;
  }
}
</style>

<script>
export default {
  data() {
    return {
      umid: '',
      scanned: false,
      debt: '0000.00',
      announcements: [],
      interval: '',
    }
  },
  // this hook runs when page is being loaded
  created: function () {
    // fetch data for login page on creation
    this.getPageData()
    // set data to be refreshed every 30 seconds
    this.interval = setInterval(this.getPageData, 900000);
  },
  // this hook runs after page has been rendered
  mounted: function() {
    // get height of keypad header
    const header_height = document.querySelector(".card-header").clientHeight;
    // dynamically set height of keypad
    const keypad_height = `calc(100% - ${header_height}px)`;
    document.querySelector(".cb-kp-container").style.height = keypad_height;
  },
  beforeDestroy: function () {
    this.interval = clearInterval(this.interval)
  },
  methods: {
    /**
     * AJAX requests
     */
    getPageData() {
      const url = 'http://localhost:6543/api/terminal/login'
      this.$axios.post(url, {
        token: 'ABC123',
      }).then(result => {
        this.announcements = result.data.announcements
        this.debt = result.data.debt
      })
      .catch(error => {
        console.log(error)
      })
    },
    checkUmid() {
      const url = 'http://localhost:6543/api/terminal/umid'
      this.$axios.post(url, {
          umid: this.umid,
          scanned: this.scanned,
          token: 'ABC123',
      })
      .then((response) => {
        this.$router.push({ name: 'terminal', params: { data: response.data }})
      })
      .catch((error) => {
        console.log(error)
        this.toggleModal() // displayed on failure to validate umid
      })
    },

    /**
     * Keypad toggles / click handlers
     */
    toggleModal() {
      const modal = document.querySelector(".modal");
      if (modal.classList.contains("is-active")) {
        modal.classList.remove("is-active");
      } else {
        // clear umid data and reset progress bar
        this.scanned = null;
        this.umid = "";
        document
          .querySelector(".progress")
          .setAttribute("value", this.umid.length);
        modal.classList.add("is-active");
      }
    },
    handleKeypadEntry(key) {
      if (Number.isInteger(key)) {
        this.umid += key;
        if (this.umid.length === 8) {
          document.querySelector('.progress').removeAttribute('value')
          this.checkUmid()
          return
        }
      } else {
        if (key === 'Clear') {
          this.umid = ''
        }
        else if (key === 'Delete') {
          this.umid = this.umid.slice(0, -1)
        }
      }

      document.querySelector('.progress').setAttribute('value', this.umid.length)
    }
  }
};
</script>
