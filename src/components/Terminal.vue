<template>
  <div class="container">
    <div class="row">
        <div class="col-md-2">
          <div class="row well">
            <img src="../assets/chezbetty_1000px.jpg" class="pull-left" style="margin-top:5px;width:100px;" />
            <h4 class="pull-right" style="width: 100px;">Administrator</h4>
          </div>

          <div id="user-info-current-balance" class="row well balance-box ">
            <h4>Your Current Balance</h4>
            <span class="current-formatted-balance"><span class="positive">$0.00</span></span>
          </div>

          <div id="user-info-new-balance" class="row well balance-box ">
            <h4>Balance after Purchase or Deposit</h4>
            <span><span class="positive">$0.00</span></span>
          </div>

          <div id="pool-info-current-balance" class="row well balance-box" style="display:none;">
            <h4>Selected Pool Balance</h4>
            <span></span>
          </div>

          <div id="user-balance" class="hidden">0E-10</div>
          <div id="user-umid" class="hidden">99999999</div>
          <div id="user-role" class="hidden">administrator</div>





          <div class="panel panel-default row">
            <div class="panel-heading">
              <h3 class="panel-title" style="font-size:150%;">Cash Deposit</h3>
            </div>
            <div class="panel-body">

              <div id="deposit-alerts"></div>

              <div id="deposit-main" >
                <div class="row">
                  <div class="col-md-12">
                    <h5 style="font-size:150%;">To make a cash deposit, put money in the bill acceptor. It will automatically be added to your account.</h5>
                  </div>
                </div>
              </div>

              <div id="deposit-complete" style="display:none;">
                <div class="row">
                  <div class="col-md-12">

                    <div style="text-align:center;">
                      <span class="deposit-thankyou">Thank you!</span>
                    </div>

                    <p>
                      <span id="deposit-complete-user">
                        You successfully deposited <span class="deposit-amount"></span> into your account.
                      </span>
                    </p>

                    <p>
                      You can continue to insert bills into the bill acceptor.
                      They will be added to your deposit.
                    </p>

                  </div>
                </div>
              </div>

              <div id="deposit-counting" class="row" style="display:none;">
                <div class="col-md-12">
                  <h3>Processing the inserted bill...</h3>
                </div>
              </div>

            </div>
          </div>

        </div>

        <div class="col-md-10">

          <div id="panel-purchase" class="panel panel-default">
            <div class="panel-heading">
              <h3 class="panel-title">Purchase</h3>
            </div>
            <div class="panel-body">

              <div id="purchase-alerts"></div>

              <div id="purchase-entry" class="row">
                <div class="col-md-9">
                  <table class="table table-bordered" id="purchase-table">
                    <thead>
                      <tr>
                        <th style="width: 6%">&nbsp;</th>
                        <th>Item</th>
                        <th style="width: 20%" colspan="3">Quantity</th>
                        <th style="width: 10%">Item Price</th>
                        <th style="width: 10%">Total Price</th>
                      </tr>
                    </thead>

                    <tbody>
                      <tr id="purchase-empty">
                        <td colspan="7">
                        <h3>Order Empty</h3>
                        Scan an item to begin
                        </td>
                      </tr>
                    </tbody>

                    <tfoot>
                      <tr id="purchase-row-subtotal" style="display:none;">
                        <td colspan="6"><b>Subtotal</b></td>
                        <td id="purchase-subtotal">$0.00</td>
                      </tr>
                      <tr id="purchase-row-goodstanding" >
                        <td colspan="2"><b>Good Standing Discount</b></td>
                        <td id="purchase-discount-percent" colspan="4">(20%)</td>
                        <td id="purchase-discount">($0.00)</td>
                      </tr>
                      <tr id="purchase-row-wallshame"
                          style="display:none;"

                          >
                        <td colspan="2"><b>Debtor&#39;s Fee</b></td>
                        <td id="purchase-fee-percent" colspan="4"><span id="purchase-fee-percent-amount">0</span>%</td>
                        <td id="purchase-fee">$0.00</td>
                      </tr>
                      <tr>
                        <td colspan="6"><b>Total</b></td>
                        <td id="purchase-total">$0.00</td>
                      </tr>
                    </tfoot>
                  </table>

                </div>

                <div class="col-md-3">

                  <div class="list-group">
                    <button type="button" class="list-group-item list-group-item-info list-group-item-header">Select Payment</button>
                    <button type="button" id="payment-user" class="list-group-item purchase-payment active">Your Account</button>
                  </div>


                  <div style="margin-bottom: 10px;">
                    <button type="button" id="btn-nobarcode" class="btn btn-default btn-lg btn-primary" style="width: 100%; height: 150px">
                    Item Without Barcode
                    </button>
                  </div>

                </div>

              </div>

              <div id="purchase-complete" class="row" style="display:none;">
                <div class="col-md-12">

                <div id="purchase-complete-table"></div>
                <div id="purchase-eventid" class="hidden"></div>

                </div>
              </div>

              <hr />
                <h4>Quick-Select Some Recently Purchased Items</h4>
                <div id="recently-purchased" class="row">
                  <div class="col-md-1"></div>
                </div>
              <hr />

              <div id="purchase-buttons" class="row">
                <div class="col-md-12">
                <button type="button" id="purchase-button-logout" class="btn btn-success btn-lg btn-submit btn-submit-purchase">Logout</button>
                <button type="button" id="purchase-button-purchaselogout" class="btn btn-success btn-lg btn-submit btn-submit-purchase" style="display:none;">Purchase &amp; Logout</button>
                <button type="button" id="purchase-button-purchase" class="btn btn-success btn-lg btn-submit btn-submit-purchase" style="display:none;">Purchase</button>
                </div>
              </div>

            </div>
          </div>

          <div id="panel-nobarcode" class="panel panel-default" style="display:none;">
            <div class="panel-heading">
              <h3 class="panel-title">Select Item Without Barcode</h3>
            </div>

            <div class="panel-body">
              <div id="tags">
                <h3>Choose an Item Category</h3>
                <div>
                <button type="button" id="btn-nobarcode-tags-back" class="btn btn-warning btn-back">Back</button>
                </div>
              </div>

              <div id="tag-items" style="display:none;">
                <div id="tag-items-content"></div>
                <div style="clear:left;">
                  <button type="button" id="btn-nobarcode-tag-items-back" class="btn btn-warning btn-back">Back</button>
                </div>
              </div>
            </div>
          </div>

        </div>
    </div>
  </div>
</template>


<style scoped>
  @media (min-width: 992x) {
    .container {
      width: 1600px;
    }
  }
  /*
    Generic Styles from chezbeddy-common.css
  */

  /* Color dollar amounts */
  .negative {
    color: red;
  }

  .positive {

  }

  /* Random Effects */

  /* Put a light yellow background behind text */
  .highlight {
    background-color: #fffacd;
    padding: 2px 5px 2px 5px;
  }

  .deleted {
    background-color: #f0f0f0;
    text-decoration: line-through;
    display: none;
  }

  /* Highlight a form element that's required that was not filled out */
  .form-required-missing {
    background-color: #ff8080;
    padding: 2px 5px 2px 5px;
  }
  .form-required-message {
    color: red;
    display: none;
  }

  /* Support for auto-sizing text */
  .fitin {
    overflow: hidden;
  }






  /*
    Terminal Interface Styles from chezbetty-terminal.css
  */


  /* Purchase Account Selection */
  button.list-group-item {
    width: 100%;
    text-align: left;
  }

  button.list-group-item-header {
    font-weight: bold;
  }

  /* Left sidebar */
  .logo-box {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 30px;
  }

  .balance-box {
    text-align: center;
  }

  .balance-box span {
    font-size: 16px;
  }

  h2.big-debt {
    text-align: center;
    padding-top: 5px;
    padding-bottom: 5px;
    margin-top: 0;
  }

  .big-debt {
    background-color: #A94442;
    color: white;
  }

  .big-debt .negative {
    background-color: white;
    font-size: 18px;
    padding: 5px 10px 5px 10px;
    font-weight: bold;
    margin: 3px;
  }

  /* Buttons */
  .btn-huge {
    padding: 20px 30px;
    font-size: 18pt;
  }

  .btn-submit {
    width: 100%;
    height: 100px;
    margin-bottom: 20px;
  }

  .buttons a {
    margin-right: 20px;
  }

  .btn-bordered {
    border: 1px solid #428bca;
  }

  .btn-full-width {
    width: 100%;
  }

  /* Alerts */
  #alerts {
    margin-top: 10px;
  }

  .alert {
    margin-top: 15px;
  }


  /* Purchase */
  #purchase-empty {
    text-align: center;
  }

  #purchase-empty td {
    padding: 30px 0;
  }

  .purchase-item {

  }

  #purchase-total, #purchase-subtotal, #purchase-discount, #purchase-discount-percent, #purchase-fee, #purchase-fee-percent {
    text-align: right;
    font-weight: bold;
  }

  #purchase-discount, #purchase-discount-percent {
    color: red;
  }

  .btn-nobarcode-tag {
    width: 200px;
    height: 75px;
    font-size: 18px;
    margin-right: 10px;
    margin-bottom: 10px;
  }

  .tag-item {
    border: 1px solid #ccc;
    text-align: center;
    padding: 6px;
    width: 200px;
    height: 225px;
    margin-right: 10px;
    margin-bottom: 10px;
    float: left;
  }

  /* Center an image and automatically scale to its containing box */
  .item-img-boundingbox {
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    height: 80%;
    width: 100%;
  }

  .btn-back {
    width: 250px;
    height: 100px;
    margin-top: 25px;
    font-size: 18pt;
  }


  /* Deposit */
  .deposit-thankyou {
    font-size: 48px;
  }

  .deposit-amount {
    color: #3071a9;
    font-size: 34px;
  }

  .btn-text-alt {
    display: none;
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
