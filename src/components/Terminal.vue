<template>
  <section class="section is-clipped">
    <div class="tile is-ancestor">
      <div class="tile is-parent is-vertical is-2">

        <!-- tile with chez betty image and name of logged in user-->
        <div class="tile is-child">
          <div class="card">
            <div class="card-image">
              <figure class="image is-square">
                <img src="../assets/chezbetty_1000px.jpg" alt="Logo" />
              </figure>
            </div>
            <div class="card-footer">
              <p class="card-footer-item">
                <span><b>{{ username }}</b></span>
              </p>
            </div>
          </div>
        </div>

        <!-- tile with current balance -->
        <div class="tile is-child notification is-info cb-left-tile">
            <p class="title">Current Balance</p>
            <p class="subtitle"><br>${{ balance.toFixed(2) }}</p>
        </div>

        <!-- tile with balance to be expected after purchase -->
        <div class="tile is-child notification is-info cb-left-tile">
          <p class="title">Expected Balance</p>
          <p class="subtitle"><br>${{ (balance - finalTotal).toFixed(2) }}</p>
        </div>

        <!-- tile with cash deposit process explanation -->
        <div class="tile is-child notification is-info cb-left-tile">
          <p class="title">Cash Deposits</p>
          <p class="subtitle">
            To make a cash deposit, insert money in the bill acceptor on your right. 
            It will automatically be added to your account.
          </p>
        </div>
      </div>
      <div class="tile is-parent is-10">
        <div class="tile is-child">
          <div class="panel is-info">
            <p class="panel-heading">Purchase (Using {{ currentPaymentMethod }} Balance)</p>
            <div class="panel-block">
              <div class="tile">
                <div class="tile is-parent is-9">
                  <div class="tile is-child">

                    <!-- table containing purchases, discounts, and total -->
                    <table class="table is-bordered is-fullwidth">
                      <thead>
                        <tr>
                          <th>Remove</th>
                          <th>Item</th>
                          <th>Amount</th>
                          <th>Price</th>
                          <th>Total Price</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-if="cart_total === 0">
                          <td colspan="5">
                            <b>Cart empty. Scan an item to begin!</b>
                          </td>
                        </tr>
                        <tr v-for="item in cart" :key="item.id">
                          <td>
                            <button class="remove" v-on:click="removeItem(item.id)">-</button>
                          </td>
                          <td>{{ item.name }}</td>
                          <td>{{ item.amount }}</td>
                          <td>${{ item.price }}</td>
                          <td></td>
                        </tr>
                      </tbody>
                      <tfoot>
                        <tr>
                          <td colspan="4">Subtotal</td>
                          <td>${{ cart_total.toFixed(2) }}</td>
                        </tr>
                        <tr>
                          <td colspan="3">{{ discount_type }}</td>
                          <td colspan="1">{{ discount }}%</td>
                          <td colspan="1">-${{ saved }}</td>
                        </tr>
                        <tr>
                          <td colspan="4">Total</td>
                          <td>${{ finalTotal }}</td>
                        </tr>
                      </tfoot>
                    </table>
                  </div>
                </div>

                <!-- buttons to select payment method, pull up listing of no barcode items -->
                <div class="tile is-parent is-3">
                  <div class="tile is-child">
                    <div class="buttons">
                      <button :disabled="Object.entries(purchase_pools).length === 0" class="button is-success is-fullwidth" @click="poolModal = true">
                        Select Purchase Pool
                      </button>
                      <button class="button is-success is-fullwidth" @click="noBarcodeModal = true">
                        Item Without Barcode
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- checkout / logout button that redirects to a receipt page or the login page -->
            <div id="checkout">
              <button class="button is-large is-success is-fullwidth" @click="checkOut()">
                {{ cart_total !== 0 ? 'Checkout' : 'Logout' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- modal popup for items with no barcode -->
    <div :class="{ 'is-active': noBarcodeModal }" class="modal">
      <div class="modal-background" @click="noBarcodeModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Select Relevant Tag</p>
          <button class="delete" @click="noBarcodeModal = false"></button>
        </header>
        <section class="modal-card-body">
          <div class="tabs is-centered is-fullwidth">
            <ul>
              <li :class="{ 'is-active': currentTag === 'Other' }" @click="getItemsByTagId('Other')"><a>Other</a></li>
              <li :class="{ 'is-active': currentTag === tag.id}" v-for="tag in tagsWithNoBarcodeItems" :key="tag.id" @click="getItemsByTagId(tag.id)"><a>{{ tag.name }}</a></li>
            </ul>
          </div>
          <p class="has-text-centered" v-if="Object.entries(currentTagItems).length === 0">{{ defaultTagMsg }}</p>
          <div class="buttons">
            <button class="button is-success" v-for="item in currentTagItems" :key="item.id" @click="addItemById(item.id)">{{ item.name }}</button>
          </div>
        </section>
      </div>
    </div>

    <!-- modal popup for failed item scans -->
    <div :class="{ 'is-active': scanModal }" class="modal">
      <div class="modal-background" @click="displayScanModal = false"></div>
      <div class="modal-content">
        <div class="notification is-danger is-size-4">
            That barcode was not recognized. Try scanning the item again. If it fails again
            the item likely is not part of the offical Chez Betty inventory.
        </div>
      </div>
      <button class="modal-close is-large" @click="displayScanModal = false"></button>
    </div>

    <!-- modal popup for successful deposit -->
    <div :class="{ 'is-active': depositModal}" class="modal">
      <div class="modal-background" @click="displayDepositModal = false"></div>
      <div class="modal-content">
        <div class="notification is-success">
          <p class="title">Your deposit was successful!</p>
          <p class="subtitle">Deposit Amount: {{ depositResponse.amount }}</p>
          <p class="subtitle">New Balance: {{ depositResponse.user_balance }}</p>
          <p class="subtitle">Deposit ID: {{ depositResponse.id }}</p>
        </div>
      </div>
      <button class="modal-close is-large" @click="displayDepositModal = false"></button>
    </div>

    <!-- modal popup for failed deposit -->
    <div :class="{ 'is-active': failedDepositModal }" class="modal">
      <div class="modal-background" @click="displayFailedDepositModal = false"></div>
      <div class="modal-content">
        <div class="notification is-danger is-size-4">
            Uh oh. It looks like your deposit has failed. To resolve this, please
            email the Chez Betty staff (chezbetty@umich.edu) at your earliest convenience!
        </div>
      </div>
      <button class="modal-close is-large" @click="displayFailedDepositModal = false"></button>
    </div>

    <!-- modal popup for purchase pools -->
    <div :class="{ 'is-active': poolModal }" class="modal">
      <div class="modal-background" @click="poolModal = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Select a Payment Method</p>
          <button class="delete" @click="poolModal = false"></button>
        </header>
        <section class="modal-card-body">
          <div class="buttons">
            <button class="button is-success" @click="selectPool('user')">Account</button>
            <button class="button is-success" v-for="pool in purchase_pools" :key="pool.id" @click="selectPool(pool.id)">{{ pool.name }}</button>
          </div>
        </section>
      </div>
    </div>

    <!-- modal popup for successful purchase -->
    <div :class="{ 'is-active': purchaseModal }" class="modal">
      <div class="modal-background" @click="logOut()"></div>
      <div class="modal-content">
        <div v-if="Object.entries(purchaseResponse).length > 0" class="notification is-success">
          <p class="title">Your purchase was successful!</p>
          <p class="subtitle">Total: ${{ parseFloat(purchaseResponse.order_table.order.total).toFixed(2) }}</p>
          <p class="subtitle">Payment Method: {{ currentPaymentMethod }}
          <p class="subtitle">New Balance: ${{ purchaseResponse.order_table.pool_balance !== '' ? purchaseResponse.order_table.pool_balance : parseFloat(purchaseResponse.user_balance).toFixed(2) }}</p>
          <p class="subtitle">Purchase ID: {{ purchaseResponse.order_table.event_id }}</p>
        </div>
      </div>
      <button class="modal-close is-large" @click="logOut()"></button>
    </div>

    <!-- modal popup for failed purchase -->
    <div :class="{ 'is-active': purchaseFailedModal}" class="modal">
      <div class="modal-background" @click="logOut()"></div>
      <div class="modal-content">
        <div class="notification is-danger">
          <p class="title">
            Your purchase has failed. If you are able please email the Chez Betty team 
            at chezbetty@umich.edu with the circumstances of the failure. We'll do our best
            to fix it!
          </p>
        </div>
      </div>
      <button class="modal-close is-large" @click="logOut()"></button>
    </div>

    <!-- modal popup for debt reminder -->
    <div :class="{ 'is-active': debtModal}" class="modal">
      <div class="modal-background" @click="debtModal = false"></div>
      <div class="modal-content">
        <div class="notification is-danger">
          <p class="title">
            Hi {{ username }}, you currently owe Betty {{ balance.toFixed(2) }}.
          </p>
          <p class="subtitle">
            Remember, Betty is NOT linked to your UM account! The only ways to add funds are 
            the bill acceptor and through the web portal using your credit card. Please try
            to pay Betty back soon!
          </p>
        </div>
      </div>
      <button class="modal-close is-large" @click="debtModal = false"></button>
    </div>
  </section>
</template>

<style scoped lang="scss">
  // helper to vertically center items
  .is-vertical-centered {
    display: flex;
    align-items: center;
  }

  .button {
    height: 5rem;
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

  .card-image {
    img {
      width: 100%;
    }
  }

  .cb-left-tile {
    p .title {
      font-size: 1rem;
    }

    p .subtitle {
      font-size: 1rem;
    }
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
      cb_url: 'http://localhost:6543',
      token: 'ABC123',

      username: '',
      balance: 0,
      umid: '',
      purchase_pools: {},
      currentPaymentMethod: 'Account',

      cart: {},
      cart_total: 0,
      discount: 0,
      discount_type: 'None',
      selected_pool: null,

      depositAmount: 0,
      barcode: '',

      tagsWithNoBarcodeItems: {},
      depositResponse: {},
      purchaseResponse: {},
      defaultTagMsg: 'Select a Tag to Search For Items',
      currentTagItems: {},
      currentTag: null,
      timeout: '',

      depositModal: false,
      failedDepositModal: false,
      scanModal: false,
      noBarcodeModal: false,
      poolModal: false,
      purchaseModal: false,
      purchaseFailedModal: false,
      debtModal: false,
    };
  },

  computed: {
    saved() {
      let ct = parseFloat(this.cart_total)
      return parseFloat(ct * (this.discount / 100)).toFixed(2)
    },
    finalTotal() {
      let ct = parseFloat(this.cart_total)
      return parseFloat(ct - (ct * this.discount / 100)).toFixed(2)
    },
  },

  created: function() {
    this.username = this.$route.params.data.user_name
    this.balance = parseFloat(this.$route.params.data.user_balance)
    this.umid = this.$route.params.data.user_umid
    this.role = this.$route.params.data.user_role
    this.purchase_pools = this.$route.params.data.purchase_pools
    this.discount = parseFloat(this.$route.params.data.discount)
    this.discount_type = this.$route.params.data.discount_type
    this.tagsWithNoBarcodeItems = this.$route.params.data.tags_with_nobarcode_items

    if (this.balance < -5.00) {
      this.debtModal = true
    }

    this.timeout = setInterval(this.handleHeartbeat, 5000)
  },

  beforeDestroy: function() {
    this.timeout = clearInterval(this.timeout)
  },

  methods: {
    // ensure cb is still online
    handleHeartbeat() {
      const url = 'http://localhost:6543/api/terminal/heartbeat'
      this.$axios.post(url, {
        token: 'ABC123',
      }).then(() => {
        this.timeoutModal = false
      }).catch(() => {
        this.$router.push({ name: 'login', params: { 'timeout': true} })
      })
    },

    // all items added by id are already in client side vars by now
    addItemById(id) {
      if (id in this.cart) {
        this.cart[id].amount += 1
      } else {
        // deep copy
        let item_dict = {
          'id': this.currentTagItems[id].id,
          'name': this.currentTagItems[id].name,
          'price': this.currentTagItems[id].price,
          'amount': 1,
        }
        this.cart[id] = item_dict
      }
      this.cart_total += parseFloat(this.cart[id].price)
    },

    // get dict of items associated with this tag
    getItemsByTagId(id) {
      // set tag as active
      this.currentTag = id

      const url = `${this.cb_url}/api/terminal/tag`
      this.$axios.post(url, {
        token: this.token,
        id: id,
      }).then((response) => {
        console.log(response.data)
        this.currentTagItems = response.data
        if (Object.entries(this.currentTagItems).length === 0) {
          this.defaultTagMsg = 'There currently are no items for this tag.'
        }
      }).catch((error) => {
        this.defaultTagMsg = 'Error loading items...'
        this.currentTagItems = {}
        console.log(error)
      })
    },

    // items with barcodes need to have their data fetched via api
    addItemWithBarcode(barcode) {
      const url = `${this.cb_url}/api/terminal/id`
      this.$axios.post(url, {
        token: this.token,
        barcode: barcode,
      }).then((response) => {
        let id = response.data.id
        if (id in this.cart) {
          this.cart[id].amount += 1
        } else {
          // deep copy
          let item_dict = {
            'id': id,
            'name': response.data.name,
            'price': response.data.price,
            'amount': 1,
          }
          this.cart[id] = item_dict
        }
        this.cart_total += parseFloat(this.cart[id].price)
      }).catch((error) => {
        console.log(error)
        this.displayScanModal = true
      })
    },

    // select a pool
    selectPool(id) {
      if (id === 'user') {
        this.selected_pool = ''
        this.currentPaymentMethod = 'Account'
        this.balance = parseFloat(this.$route.params.data.user_balance)
      } else{
        this.selected_pool = id
        this.currentPaymentMethod = this.purchase_pools[id].name
        this.balance = parseFloat(this.purchase_pools[id].balance)
      }
      this.poolModal = false
    },

    // remove an item from the cart
    removeItem(id) {
      this.cart[id].amount -= 1
      this.cart_total -= parseFloat(this.cart[id].price)

      if (this.cart[id].amount <= 0) {
        delete this.cart[id]
      }
    },

    // checkout with items in cart
    checkOut() {
      if (this.cart_total === 0) {
        this.logOut()
        return
      }
      const url = `${this.cb_url}/api/terminal/purchase`
      this.$axios.post(url, {
        token: this.token,
        umid: this.umid,
        items: this.cart,
        pool_id: this.selected_pool,
      })
      .then((response) => {
        this.purchaseResponse = response.data
        this.purchaseModal = true
      })
      .catch(error => {
        this.purchaseFailedModal = true
        console.log(error)
      })
    },

    // someone used the bill acceptor while logged in
    addFunds() {
      const url = `${this.cb_url}/api/terminal/deposit`
      this.$axios.post(url, {
        umid: this.umid,
        token: this.token,
        amount: this.depositAmount,
        method: 'acceptor',
      })
      .then((response) => {
        this.balance = response.data.user_balance
        this.depositResponse = response.data
        this.displayDepositModal = true
      })
      .catch(error => {
        console.log(error)
        this.displayFailedDepositModal = true
      });
    },

    // log current user out
    logOut() {
      this.$router.push({ name: 'login', params: {} })
    },

    handleBarcodeScane() {
      // function stub for barcode scanner. should read the barcode
      // using something like node-hid, then call addItemWithBarcode()
    },
    handleBillAcceptor() {
      // function stub for bill acceptor. depending on how you want to handle this,
      // it might be best to make this a global listener to at least log all
      // bills that have been accepted, rather than only running on the terminal page.
    }
  },
};
</script>
