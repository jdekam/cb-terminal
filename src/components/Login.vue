<template>
  <div class="container">
    <div id="request-device">BUTTON</div>
    <div id="wrap">
      <div id="content" class="container">
        <div id="index" class="row">
          <div class="col-md-7">
            <div class="row">
              <div class="col-md-12">
                <h1 style="font-size:375%;">
                  <img src="../assets/chezbetty_1000px.jpg" style="margin-top:5px;width:180px;" />
                  Current User Debt: <strong><span class="positive">$0.00</span></strong>
                </h1>
              </div>
            </div>
            <div class="row">
              <div class="col-md-12">
                <div id="alerts"></div>
                <div id="announcements" style="font-size:20pt;"></div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-12"></div>
            </div>
          </div>
          <div class="col-md-5" style="text-align: center;">
            <div id="index-main" style="margin-top:100px;">
              <h2>Swipe your M-Card to login</h2>
            </div>
            <hr />
            <div class="or"><span>OR</span></div>
            <div class="center">
              <h2>Enter your UMID here</h2>
            </div>
            <link rel="stylesheet" href="http://127.0.0.1:6543/static/css/chezbetty-terminal-keypad.css" />
            <div id="keypad-umid" class="center keypad-lg">
              <container>
                <container id="keypad-umid-status">
                  <block class="umid-status-block btn btn-default"></block>
                  <block class="umid-status-block btn btn-default"></block>
                  <block class="umid-status-block btn btn-default"></block>
                  <block class="umid-status-block btn btn-default"></block>
                  <block class="umid-status-block btn btn-default"></block>
                  <block class="umid-status-block btn btn-default"></block>
                  <block class="umid-status-block btn btn-default"></block>
                  <block class="umid-status-block btn btn-default"></block>
                </container>
                <block><button type="button" id="btn-keypad-9" class="btn btn-default btn-keypad">9</button></block>
                <block><button type="button" id="btn-keypad-8" class="btn btn-default btn-keypad">8</button></block>
                <block><button type="button" id="btn-keypad-7" class="btn btn-default btn-keypad">7</button></block>
                <block><button type="button" id="btn-keypad-6" class="btn btn-default btn-keypad">6</button></block>
                <block><button type="button" id="btn-keypad-5" class="btn btn-default btn-keypad">5</button></block>
                <block><button type="button" id="btn-keypad-4" class="btn btn-default btn-keypad">4</button></block>
                <block><button type="button" id="btn-keypad-3" class="btn btn-default btn-keypad">3</button></block>
                <block><button type="button" id="btn-keypad-2" class="btn btn-default btn-keypad">2</button></block>
                <block><button type="button" id="btn-keypad-1" class="btn btn-default btn-keypad">1</button></block>
                <block><button type="button" id="btn-keypad-clear" class="btn btn-default btn-keypad">Clear</button></block>
                <block><button type="button" id="btn-keypad-del" class="btn btn-default btn-keypad">&laquo;</button></block>
                <block><button type="button" id="btn-keypad-0" class="btn btn-default btn-keypad">0</button></block>
              </container>
            </div>
          </div>
        </div>
        <!--
        <div id="splash" class="container">
          <h1>We're glad everyone is using Betty, but we do need to get paid back.</h1>
          <h1>The current user debt is: <strong><span class="positive">$0.00</span></strong>.</h1>
          <h1>We could use some help getting that repaid.</h1>
          <h1>So please, if you owe Betty money pay back today.</h1>
          <div class="pull-right">
            <br />
            <h4>
              Also, you get a 5% discount if you have at least $20 in your account.
              Users who are more than $5 in debt are taxed on every purchase.
            </h4>
          </div>
          <div class="pull-left">
            <a class="btn btn-deftaul btn-huge btn-bordered" onclick='$("#splash").hide(); $("#index").show(); $("#footer").show();'>Continue to Betty</a>
          </div>
          <div class="clearfix"></div>
        </div>
        -->
      </div>
      <div id="footer" class="navbar navbar-fixed-bottom" role="navigation" style="width:50%">
        <div class="container-fluid">
          <hr />
          <p>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-en">English</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-de">Deutsch</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-fr">français</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-tw">漢語</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-cn">简体中文</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-fa">فارسی</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-ro">Română</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-es">Español</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-ar">العربية</a>
          </p>
          <p>
            <strong>Can you help translate Betty? github.com/cseg-michigan/chez-betty</strong>
          </p>
          <hr />
        </div>
      </div>
    </div>

    <!--
    <script src="http://127.0.0.1:6543/static/js/chezbetty-terminal.js"></script>
    <script src="http://127.0.0.1:6543/static/js/chezbetty-common-onload.js"></script>
    <script src="http://127.0.0.1:6543/static/js/chezbetty-terminal-keyboard.js"></script>
    <script src="http://127.0.0.1:6543/static/js/chezbetty-terminal-hid.js"></script>
    -->

    <!--
    <script>
      if ($('#splash').length != 0) {
        $("#index").hide();
        $("#footer").hide();
        $("#splash").show();
      }
    </script>
    -->

    <!--
    <script>
      var wintimeout = setTimeout(terminal_timeout, 14400000);

      // Called on each mouse click (user touching screen)
      $(document).mousedown(function(e) {
        // Reset the timeout timer
        if (wintimeout) {
          clearTimeout(wintimeout);
        }
        // Start a new timeout in case this is the last keypress (1min timeout)
        wintimeout = setTimeout(terminal_timeout, 14400000);
      });

      // Called on each keypress (barcode scan)
      $(document).keypress(function(e) {
        // Reset the timeout timer
        if (wintimeout) {
          clearTimeout(wintimeout);
        }
        // Start a new timeout in case this is the last keypress (1min timeout)
        wintimeout = setTimeout(terminal_timeout, 14400000);
      });
    </script>
    -->


    <!-- Google Analytics tracker -->
    <!--
    <script>
      (function(i, s, o, g, r, a, m) {
        i['GoogleAnalyticsObject'] = r;
        i[r] = i[r] || function() {
          (i[r].q = i[r].q || []).push(arguments)
        }, i[r].l = 1 * new Date();
        a = s.createElement(o),
          m = s.getElementsByTagName(o)[0];
        a.async = 1;
        a.src = g;
        m.parentNode.insertBefore(a, m)
      })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

      ga('create', 'UA-55624000-1', 'auto');
      ga('send', 'pageview');
    </script>
    -->

    <!--
    <link rel="stylesheet" type="text/css" href="http://127.0.0.1:6543/_debug_toolbar/static/toolbar/toolbar_button.css" />

    <div id="pDebug">
      <div id="pDebugToolbarHandle">
        <a title="Show Toolbar" id="pShowToolBarButton" href="http://127.0.0.1:6543/_debug_toolbar/313430333632373034303039363830" target="pDebugToolbar">&#171;</a>
      </div>
    </div>
    -->
  </div>
</template>

<!--
<template>
  <div class="row">
    <div class="col-md-7">

      <div class="row">
        <div class="col-md-12">
          <h1 style="font-size:375%;">
          <img src="../assets/chezbetty_1000px.jpg" style="margin-top: 5px; width: 180px;">
          Current User Debt: <strong>{{ debt }}</strong>
          </h1>
        </div>
      </div>


      <div class="row">
        <div class="col-md-12">
          <div id="announcements" style="font-size:20pt;">
            <div
              class="alert alert-info" role="alert"
              v-for="announcement in announcements"
              :key="announcement.id"
            >
              {{ announcement.content }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="col-md-5" style="text-align: center;">

      <div style="margin-top:100px;">
        <h2>Swipe your M-Card to login</h2>
      </div>
      <hr>
      <div class="or"><span>OR</span></div>
      <div class="center">
        <h2>Enter your UMID here</h2>
      </div>
    </div>
  </div>
</template>
-->

<style scoped>
@import '../assets/Login.css';
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
