<template>
  <section class="section is-clipped">
    <div class="tile is-ancestor">
      <div class="tile is-parent is-vertical is-2">
        <div class="tile is-child">
          <div class="card">
            <figure class="image is-square">
              <img src="../assets/chezbetty_1000px.jpg" alt="CB Logo" />
            </figure>
            <p>{{ username }}</p>
          </div>
        </div>
        <div class="tile is-child notification is-info cb-left-tile">
          <p class="title">Your Current Balance</p>
          <p class="subtitle">${{ balance }}</p>
        </div>
        <div class="tile is-child notification is-info cb-left-tile">
          <p class="title">Balance after Purchase or Deposit</p>
          <p class="subtitle">${{ balance_after }}</p>
        </div>
        <div class="tile is-child notification is-info cb-left-tile">
          <p class="title">Cash Deposit</p>
          <!--<p class="subtitle">
            To make a cash deposit, put money in the bill acceptor. It will automatically be added to your account.
          </p>-->
        </div>
      </div>
      <div class="tile is-parent is-10">
        <div class="tile is-child">
          <div v-if="!noBarSearch && !addingMoney" class="panel is-info">
            <p class="panel-heading">Purchase</p>
            <div class="panel-block">
              <div class="tile">
                <div class="tile is-parent is-9">
                  <div class="tile is-child">
                    <table class="table is-bordered is-fullwidth">
                      <thead>
                        <tr>
                          <th>Remove Item</th>
                          <th>Item</th>
                          <th>Quantity</th>
                          <th>Item Price</th>
                          <th>Total Price</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-if="!final_total">
                          <td colspan="5">
                            <h1>Order Empty</h1>
                            <h3>Scan an item to begin</h3>
                          </td>
                        </tr>

                        <tr v-for="(item, index) in cart" :key="index">
                          <td>
                            <button class="remove" v-on:click="removeItem(item.id)">-</button>
                          </td>
                          <td>{{item.type}}</td>
                          <td>{{item.amount}}</td>
                          <td>${{item.cost}}</td>
                          <td>${{item.total_price}}</td>
                        </tr>
                      </tbody>
                      <tfoot>
                        <tr>
                          <td colspan="4">Subtotal</td>
                          <td>{{cart_total}}</td>
                        </tr>
                        <tr>
                          <td colspan="3">Good Standing Discount</td>
                          <td colspan="1">{{discount}}%</td>
                          <td colspan="1">${{discount_savings}}</td>
                        </tr>
                        <tr>
                          <td colspan="4">Total</td>
                          <td>${{final_total}}</td>
                        </tr>
                      </tfoot>
                    </table>
                  </div>
                </div>
                <div class="tile is-parent is-3">
                  <div class="tile is-child">
                    <div class="buttons">
                      <button
                        class="button is-small is-link is-fullwidth"
                        v-on:click="selectPayment"
                      >Add Funds</button>
                      <!--<button
                        class="button is-small is-info is-fullwidth"
                        v-on:click="accountInfo"
                      >Your Account</button>-->
                      <button
                        class="button is-info is-fullwidth"
                        v-on:click="itemWithoutBarcode"
                      >Item Without Barcode</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div id="checkout" v-if="final_total">
              <button
                class="button is-large is-success is-fullwidth"
                v-on:click="checkOut"
              >Purchase And Logout</button>
            </div>
            <div id="checkout" v-else>
              <button class="button is-large is-success is-fullwidth" v-on:click="logOut">Logout</button>
            </div>
          </div>

          <div v-if="noBarSearch">
            <button
              class="button is-large is-success margin-25"
              v-for="(item, index) in no_barcode"
              :key="index"
              v-on:click="addItem(item.id)"
            >{{item.name}}</button>
          </div>

          <div v-if="addingMoney">
            Enter the Amount:
            <input type="number" step="1" min="0" max="50" v-model="addAmount" />
            <button v-on:click="addFunds">Add Funds</button>
          </div>
        </div>
      </div>
    </div>
    <div class="tile cb-translate">
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
}

style chez betty logo .card-image {
  padding: 0.75rem;

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

.cb-left-tile {
  p.title {
    font-size: 18px;
  }

  p.subtitle {
    font-size: 15px;
  }
}

.margin-25 {
  margin: 2.5%;
}

.remove {
  border-radius: 50%;
  background-color: red;
  color: white;
}
</style>

<script>
export default {
  data() {
    return {
      username: "Administrator",
      balance: "0.00",
      umid: 11111111,
      balance_after: "0.00",
      amount_owed: "0",
      no_barcode: [],
      cart: [],
      cart_total: (0.0).toFixed(2),
      discount: 5,
      discount_savings: (0.0).toFixed(2),
      final_total: 0,
      noBarSearch: false,
      addingMoney: false,
      emptyCart: true,
      addAmount: 0,
      barcode: "",
      jsonData: {}
    };
  },
  mounted: function() {
    console.log(this.$route.params.data);
    this.username = this.$route.params.data.user_name;
    this.balance = this.$route.params.data.user_balance;
    this.umid = this.$route.params.data.user_umid;
    this.discout = this.$route.params.data.good_standing_discount;
    this.no_barcode = this.$route.params.data.all_items;
    console.log(this.$route.params.data.all_items);
  },
  methods: {
    addItem(itemID) {
      console.log(itemID);
      //get cost
      let url = "http://localhost:6543/api/terminal/id";
      this.$axios
        .post(url, {
          umid: this.umid,
          token: "ABC123",
          item_id: itemID
        })
        .then(response => {
          let cost = parseFloat(response.data.price);
          for (let i = 0; i < this.cart.length; ++i) {
            if (this.cart[i].id === response.data.id) {
              this.cart[i].amount += 1;
              this.cart_total = (
                parseFloat(this.cart_total) + parseFloat(pusher.cost)
              ).toFixed(2);
              this.discount_savings = (
                parseFloat(this.discount_savings) +
                parseFloat(cost) * (parseFloat(this.discount) / 100)
              ).toFixed(2);
              this.final_total = this.cart_total - this.discount_savings;
              this.toMain();
            }
          }
          let pusher = {
            id: response.data.id,
            cost: cost.toFixed(2),
            type: response.data.name,
            amount: 1,
            total_price: cost.toFixed(2)
          };
          this.cart.push(pusher);
          this.cart_total = (
            parseFloat(this.cart_total) + parseFloat(pusher.cost)
          ).toFixed(2);
          this.discount_savings = (
            parseFloat(this.discount_savings) +
            parseFloat(cost) * (parseFloat(this.discount) / 100)
          ).toFixed(2);
          this.final_total = this.cart_total - this.discount_savings;
          this.toMain();
        });
    },
    //removes and item from the cart
    removeItem(itemID) {
      for (let i = 0; i < this.cart.length; ++i) {
        if (this.cart[i].id === itemID) {
          if (this.cart[i].amount === 1) {
            this.cart_total = (
              parseFloat(this.cart_total) - parseFloat(this.cart[i].cost)
            ).toFixed(2);
            this.discount_savings = (
              parseFloat(this.discount_savings) -
              parseFloat(this.cart[i].cost) * (parseFloat(this.discount) / 100)
            ).toFixed(2);
            this.final_total = this.cart_total - this.discount_savings;
            this.cart.splice(i, 1);
            return;
          } else {
            this.cart[i].amount -= 1;
            this.cart_total = (
              parseFloat(this.cart_total) - parseFloat(this.cart[i].cost)
            ).toFixed(2);
            return;
          }
        }
      }
    },
    checkOut() {
      let sender = [];
      for (let item in this.cart) {
        let pusher = { item_id: item.id, quantity: item.amount };
        sender.push(pusher);
      }
      let url = "http://localhost:6543/api/terminal/purchase";
      this.$axios
        .post(url, {
          umid: this.umid,
          token: "ABC123",
          items: sender
        })
        .then(() => {
          this.logOut();
          //need to pass the response up to login.vue, unsure how
        })
        .catch(error => {
          alert(error);
        });
    },
    itemWithoutBarcode() {
      this.noBarSearch = true;
    },
    toMain() {
      this.noBarSearch = false;
      this.addingMoney = false;
    },
    addFunds() {
      //api stuff to add funds to account and reload
      this.balance = (
        parseFloat(this.balance) + parseFloat(this.addAmount)
      ).toFixed(2);
      let url = "http://localhost:6543/api/terminal/deposit";
      this.$axios
        .post(url, {
          umid: this.umid,
          token: "ABC123",
          amount: this.addAmount,
          method: "acceptor"
        })
        .then(() => {
          this.toMain();
          //need to pass the response up to login.vue, unsure how
        })
        .catch(error => {
          alert(error);
        });
      this.toMain();
    },
    selectPayment() {
      this.addingMoney = true;
    },
    logOut() {
      this.$router.push({ name: "login", params: {} });
    }
  }
};
</script>
