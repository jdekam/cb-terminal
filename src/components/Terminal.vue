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
          <div class="panel is-info">
            <p class="panel-heading">Purchase</p>
            <div class="panel-block">
              <div class="tile">
                <!-- Purchase Table -->
                <!-- TODO: Figure out how to put this code into the table.
                <input type="text" v-model="barcode" v-on:keyup.enter="addItem" placeholder="Item Barcode"/>
                <div class="cart">
                  <div class="item" v-for="(item, index) in cart" :key="index">
                    <div class="costs">${{item.cost}}</div>
                    <div class="type">{{item.type}}</div>
                    <div class="amount">{{item.amount}}</div>
                  </div>
                </div>

      <div class="tile is-vertical is-parent is-10">
        <div class="tile is-child">
          <div class="card">
            
            <div v-if="!addingMoney">
              <button class="return-button" v-on:click="logOut"> LOG OUT </button>
              <input type="text" v-model="barcode" v-on:keyup.enter="addItem" placeholder="Item Barcode"/>
              <div class="cart">
                <div class="item" v-for="(item, index) in cart" :key="index">
                  <button class="remove-item" v-on:click="removeItem(item.type)">-</button>
                  <div class="costs">${{item.cost}}</div>
                  <div class="type">{{item.type}}</div>
                  <div class="amount">{{item.amount}}</div>
                </div>
                Total: ${{cart_total}}
              </div>

              <button class="submit" v-on:click="toCheckout" v-if="!checkingOut">CHECK OUT</button>
              <button class="submit" v-on:click="addFunds" v-if="!addingMoney">ADD FUNDS</button>
              <div id="checkout" v-if="checkingOut">
                Purchase these items for ${{cart_total}}?
                <button class="submit" v-on:click="checkOut">Confirm Purchase</button>
                <button class="return-button" v-on:click="toMain"> CANCEL </button>
              </div>
            </div>

            <div v-if="addingMoney">
              <button class="return-button" v-on:click="toMain"> EXIT </button>
              <p>Deposit ${{}} into your account?</p>
              <button v-on:click="addFunds"> Yes </button>
            </div>
                <button id="cart-submit" v-on:click="toCheckout" v-if="!checkingOut">CHECK OUT</button>
                <div id="checkout" v-if="checkingOut">
                  Purchase these items?
                  <button v-on:click="checkOut">Confirm Purchase</button>
                </div>
                -->
                <div class="tile is-parent is-9">
                  <div class="tile is-child">
                    <table class="table is-bordered is-fullwidth">
                      <thead>
                        <tr>
                          <th>Item</th>
                          <th>Quantity</th>
                          <th>Item Price</th>
                          <th>Total Price</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-if="emptyCart">
                          <td colspan="4">
                            <h1>Order Empty</h1>
                            <h3>Scan an item to begin</h3>
                          </td>
                        </tr>

                        <tr v-for="(item, index) in cart" :key="index">
                          <td>{{item.type}}</td>
                          <td>{{item.amount}}</td>
                          <td>${{item.cost}}</td>
                          <td>${{item.total_price}}</td>
                        </tr>
                      </tbody>
                      <tfoot>
                        <tr>
                          <td colspan="3">Subtotal</td>
                          <td>{{cart_total}}</td>
                        </tr>
                        <tr>
                          <td colspan="1">Good Standing Discount</td>
                          <td colspan="2">{{discount}}%</td>
                          <td colspan="2">${{discount_savings}}</td>
                        </tr>
                        <tr>
                          <td colspan="3">Total</td>
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
                      >Select Payment</button>
                      <button
                        class="button is-small is-info is-fullwidth"
                        v-on:click="accountInfo"
                      >Your Account</button>
                      <button
                        class="button is-info is-fullwidth"
                        v-on:click="itemWithoutBarcode"
                      >Item Without Barcode</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div id="checkout" v-if="!emptyCart">
              <button
                class="button is-large is-success is-fullwidth"
                v-on:click="checkOut"
              >Purchase And Logout</button>
            </div>
            <div id="checkout" v-else>
              <button class="button is-large is-success is-fullwidth" v-on:click="logOut">Logout</button>
            </div>
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

.type .amount {
  margin: 5%;
}

.submit {
  background-color: #2c3e50;
  color: white;
  border-radius: 15px;
  height: 20%;
}

.return-button {
  background-color: red;
  color: white;
  border-radius: 15px;
  height: 20%;
}

.remove-item {
  background-color: red;
  color: white;
  border-radius: 50%;
}
</style>

<script>
export default {
  data() {
    return {
      username: "Administrator",
      balance: "-5.00",
      umid: 11111111,
      balance_after: "-6.00",
      amount_owed: "0",
      no_barcode: [],
      cart: [
        {
          id: 1,
          cost: (2.5).toFixed(2),
          type: "Milk",
          amount: 1,
          total_price: (2.5).toFixed(2)
        }
      ],
      cart_total: (2.5).toFixed(2),
      discount: 5,
      discount_savings: (0.12).toFixed(2),
      final_total: (2.38).toFixed(2),
      checkingOut: false,
      addingMoney: false,
      emptyCart: false,
      barcode: "",
      jsonData: {}
    };
  },
  mounted: function() {
    this.username = this.$router.params.user_name;
    this.balance = this.$router.params.user_balance;
    this.umid = this.$router.params.user_umid;
    this.discout = this.$router.params.good_standing_discount;
    this.no_barcode = this.$router.params.tags_with_nobarcode_items;
  },
  methods: {
    addItem(itemID) {
      //get cost
      /**
      let url = "/terminal/item/barcode/" + this.barcode;
      this.$axios.get(url)
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
      let url = "http://localhost:6543/api/terminal/id";
      this.$axios
        .post(url, {
          umid: this.umid,
          token: "ABC123",
          item_id: itemID
        })
        .then(
          () => function(response) {
            let cost = response.price;
            for (let i = 0; i < this.cart.length; ++i) {
            if (this.cart[i].id === response.id) {
              this.cart[i].amount += 1;
              this.cart_total = (
                parseFloat(this.cart_total) + parseFloat(this.cart[i].cost)
              ).toFixed(2);
              return;
            }
          }
          let pusher = { id: response.id, cost: cost.toFixed(2), type: response.name, amount: 1 };
          this.cart.push(pusher);
          this.cart_total = (
            parseFloat(this.cart_total) + parseFloat(pusher.cost)
          ).toFixed(2);
          }
        )
    },
    //removes and item from the cart
    removeItem(itemType) {
      for (let i = 0; i < this.cart.length; ++i) {
        if (this.cart[i].type === itemType) {
          if (this.cart[i].amount === 1) {
            this.cart_total = (
              parseFloat(this.cart_total) - parseFloat(this.cart[i].cost)
            ).toFixed(2);
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
        let pusher = {item_id: item.id, quantity: item.amount};
        sender.push(pusher);
      }
      let url = "http://localhost:6543/api/terminal/purchase";
      this.$axios
        .post(url, {
          umid: this.umid,
          token: "ABC123",
          items: sender
        })
        .then(
          () =>
            function(response) {
              console.log("hello world");
              this.jsonData = response;
              console.log(this.jsonData);
              this.logOut();
              //need to pass the response up to login.vue, unsure how
            }
        );
      console.log("here2");

      /**
      let url = "/terminal/purchase";
      this.$axios.post(url, {
        username: this.username,
        total: this.cart_total,
      })
      */
    },
    /**
    itemWithoutBarcode() {
      let url = "http://localhost:6543/api/terminal/get/items";

      this.$axios.get(url) 
        .then((response) => {
          console.log(response.data);
        });
      console.log("here2");
    },*/
    toMain() {
      this.checkingOut = false;
      this.addingMoney = false;
    },
    addFunds() {
      //api stuff to add funds to account and reload
      this.toMain();
    },
    logOut() {
      this.$router.push({ name: "login", params: {} });
    }
  }
};
</script>
