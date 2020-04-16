<template>
  <section class="section is-clipped">
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-parent is-2">
        <div class="tile is-child">
          <div class="card">
            <figure class="image is-square">
              <img src="../assets/chezbetty_1000px.jpg" alt="CB Logo">
            </figure>
            <p> {{ username }} </p>
          </div>
        </div>
        <div class="tile is-child notification is-info cb-left-tile">
          <p class="title"> Your Current Balance </p>
          <p class="subtitle"> ${{ balance }} </p>
        </div>
        <div class="tile is-child notification is-info cb-left-tile">
          <p class="title"> Balance after Purchase or Deposit </p>
          <p class="subtitle"> ${{ balance_after }} </p>
        </div>
        <div class="tile is-child notification is-info cb-left-tile">
          <p class="title"> Cash Deposit </p>
          <!--<p class="subtitle">
            To make a cash deposit, put money in the bill acceptor. It will automatically be added to your account.
          </p>-->
        </div>
      </div>

        <!--
        <div class="tile is-child">
          <div class="card">
            <div class="card-content">
              <div class="notification is-info is-size-7">
                <p> Your Current Balance </p>
                <p> -$1.00 </p>
              </div>
            </div>
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
        -->

      <div class="tile is-vertical is-parent is-10">
        <div class="tile is-child">
          <div class="card">
            THIS IS THE PURCHASE SCREEN
            <input type="text" v-model="barcode" v-on:keyup.enter="addItem" placeholder="Item Barcode"/>
            <div class="cart">
              <div class="item" v-for="(item, index) in cart" :key="index">
                <div class="costs">${{item.cost}}</div>
                <div class="type">{{item.type}}</div>
                <div class="amount">{{item.amount}}</div>
              </div>
            </div>

            <button id="cart-submit" v-on:click="toCheckout" v-if="!checkingOut">CHECK OUT</button>
            <div id="checkout" v-if="checkingOut">
              Purchase these items?
              <button v-on:click="checkOut">Confirm Purchase</button>
            </div>
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
  }

  style chez betty logo
  .card-image {
    padding: .75rem;

    figure {
      width: 10vh;
    }

    img {
      width: 50%;
      height: 50%;
    }
  }

  // fix height of welcome card
  .cb-logo-username {
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

  .cb-left-tile {
    p.title {
      font-size: 18px;
    }

    p.subtitle {
      font-size: 15px;
    }
  }

  .cart {
    border-style: solid;
    padding: 5%;
    overflow: scroll;
  }

  .item {
    display: inline-block;
  }

  .costs {
    border-style: solid;
    border-width: 1px;
  }

  .type .amount{
    margin: 5%;
  }

</style>

<script>
export default {
  data() {
    return {
      username: 'Administrator',
      balance: '-5.00',
      balance_after: '-6.00',
      amount_owed: '0',
      cart: [{cost: 2.50.toFixed(2), type: "Milk", amount: 1}],
      cart_total: 0,
      checkingOut: false,
      barcode: "",
      jsonData: {},
    }
  },
  methods: {
    getUsername() {
      // api call to get username
      /**
      let url = "";
      axios.get(url)
        .then(response => function(response) {
          return response.username;
        });
      */
    },
    getBalance() {
      // api call to get user's current balance
      /**
      let url = "";
      axios.get(url)
        .then(response => function(response) {
          return response.balance;
        });
      */
    },
    getAnnouncements() {
      // api call to retreive announcements
      /**
      let url = "";
      axios.get(url)
        .then(response => function(response) {
          return response.announcements;
        });
        */
    },
    getDebt() {
      // api call to retreive user debt
      /**
      let url = "";
      axios.get(url)
        .then(response => function(response) {
          return response.currentUserDebt;
        });
        */
    },
    toCheckout() {
      this.checkingOut = true;
    },
    addItem() {
      //get cost
      /**
      let url = "";
      axios.get(url)
        .then(response => function(response) {
          this.jsonData = response;
        })
        .then(response => function() {
          let cost = 4.30;
          //let cost = this.jsonData.price;
          //let type = this.jsonData.item;
          for (let i = 0; i < this.cart.length; ++i) {
            //if (this.cart[i].type === type)
            if (this.cart[i].type === this.barcode) {
              this.cart[i].amount += 1;
              return;
            }
          }
          //let pusher = {"cost": cost.toFixed(2), "type": type:, "amount": 1}
          let pusher = {"cost": cost.toFixed(2), "type": this.barcode, "amount": 1};
          this.cart.push(pusher);
          this.cart_total += pusher.cost;
        });
        */
      let cost = 4.30;
      for (let i = 0; i < this.cart.length; ++i) {
        if (this.cart[i].type === this.barcode) {
          this.cart[i].amount += 1;
          return;
        }
      }
      let pusher = {"cost": cost.toFixed(2), "type": this.barcode, "amount": 1};
      this.cart.push(pusher);
      this.cart_total += pusher.cost;
    },
    checkOut() {
      /**
      let url = "";
      axios.post(url, {
        username: this.username,
        total: this.cart_total,
      })
      */
    },
  }
}
</script>
