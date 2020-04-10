<template>
  <section class="section is-clipped">
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-parent is-2">
        <div class="tile is-child">
          <div class="card">
            WELCOME TO CHEZ BETTY, JEREMIAH!
          </div>
        </div>
        <div class="tile is-child">
          <div class="card">
            YOUR CURRENT BALANCE IS -$1.00
          </div>
        </div>
        <div class="tile is-child">
          <div class="card">
            YOUR BALANCE AFTER PURCHASES AND DEPOSITS IS -$1.00
          </div>
        </div>
        <div class="tile is-child">
          <div class="card">
            CASH DEPOSIT FAQ
          </div>
        </div>
      </div>
      <div class="tile is-vertical is-parent is-10">
        <div class="tile is-child">
          <div class="card">
            THIS IS THE PURCHASE SCREEN
          </div>
        </div>
      </div>
    </div>
    <div class="finish">
      <div class="card is-fullwidth" style="height: 10%;">
ello mte
        </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
  // helper to vertically center items
  .is-vertical-centered {
    display: flex;
    align-items: center;
  }

  // remove overflow scrollbars
  html {
    overflow: hidden;
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
    height: 90%;
    margin: 0 !important; // this Bulma class has some weird margins by default
  }

  // make cards fill tiles
  .card {
    height: 100%;
    background-color:lightsalmon; // debug

    .card-content {
      width: 100%;
    }
  }
</style>

<script>
export default {
  data() {
    return {
      username: 'Administrator',
      balance: '-5.00',
      amount_owed: '0',
    }
  },
  methods: {
    getUsername() {
      // api call to get username
    },
    getBalance() {
      // api call to get user's current balance
    },
    getAnnouncements() {
      // api call to retreive announcements
    },
    getDebt() {
      // api call to retreive user debt
    },
  }
}
</script>
