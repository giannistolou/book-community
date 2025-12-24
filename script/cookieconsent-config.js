const APP_TYPE = '{{ type|default:"main" }}';
  const APP_CONFIGS = {
  blog: {
    gtag_id: '',
    clarity_id: '',
    plausible_domain: 'blog.book-community.com',
    sentry_dsn: 'https://3b208bcd006ce709256308f182d0c37c@sentry.io/123456',
    sentry_environment: 'blog'
  },
  cafe: {
     gtag_id: 'G-86MQLKEQCZ',
    clarity_id: 'sl12n9f03c',
    plausible_domain: 'cafe.book-community.com',
    sentry_dsn: 'https://cafe-sentry-dsn@sentry.io/456789', 
    sentry_environment: 'cafe'
  },
  main: {
    gtag_id: '',
    clarity_id: '',
    plausible_domain: 'book-community.com',
    sentry_dsn: 'https://3b208bcd006ce709256308f182d0c37c@sentry.io/123456',
    sentry_environment: 'main'
  }
};

// Get current app config
const currentAppConfig = APP_CONFIGS[APP_TYPE] || APP_CONFIGS.main;

CookieConsent.run({
  // https://cookieconsent.orestbida.com/reference/configuration-reference.html#guioptions
  guiOptions: {
    consentModal: {
      layout: "cloud inline",
      position: "bottom center",
      equalWeightButtons: true,
      flipButtons: false,
    },
    preferencesModal: {
      layout: "box",
      equalWeightButtons: true,
      flipButtons: false,
    },
  },

  onFirstConsent: ({ cookie }) => {
    console.log("onFirstConsent fired", cookie);
  },

  onConsent: ({ cookie }) => {
    console.log("onConsent fired!", cookie);
  },

  onChange: ({ changedCategories, changedServices }) => {
    console.log("onChange fired!", changedCategories, changedServices);
  },

  onModalReady: ({ modalName }) => {
    console.log("ready:", modalName);
  },

  onModalShow: ({ modalName }) => {
    console.log("visible:", modalName);
  },

  onModalHide: ({ modalName }) => {
    console.log("hidden:", modalName);
  },

  categories: {
    necessary: {
      enabled: true,
      readOnly: true,
    },
    analytics: {
      autoClear: {
        cookies: [
          {
            name: /^_ga/,
          },
          {
            name: "_gid",
          },
          {
            name: /^_gat/,
          },
          {
            name: /^_cl_/,
          },
        ],
      },

      // https://cookieconsent.orestbida.com/reference/configuration-reference.html#category-services
      services: {
        ga: {
          label: "Google Analytics",
          onAccept: () => {
            loadGoogleAnalytics();
          },
          onReject: () => {},
        },
        clarity: {
          label: "Microsoft Clarity",
          onAccept: () => {
            loadClarity();
          },
          onReject: () => {},
        },
      },
    },
    marketing: {
      autoClear: {
        cookies: [
          {
            name: "mailchimp_*",
          },
        ],
      },
      services: {
        mailchimp: {
          label: "Mailchimp Newsletter Signup",
          onAccept: () => {
            loadMailchimp();
          },
          onReject: () => {
            hideMailchimp();
          },
        },
      },
    },
  },

  language: {
    default: "el",
    translations: {
      el: {
        consentModal: {
          title: "🍪 Χρήση Cookies",
          description:
            "Χρησιμοποιούμε cookies για να βελτιώσουμε την εμπειρία σας.",
          acceptAllBtn: "Αποδοχή Όλων",
          acceptNecessaryBtn: "Μόνο Απαραίτητα",
          showPreferencesBtn: "Ρυθμίσεις",
          // closeIconLabel: 'Reject all and close modal',
          footer: `
                        <a href="#path-to-impressum.html" target="_blank">Impressum</a>
                        <a href="#path-to-privacy-policy.html" target="_blank">Privacy Policy</a>
                    `,
        },
        preferencesModal: {
          title: "Ρυθμίσεις Cookies",
          acceptAllBtn: "Αποδοχή Όλων",
          acceptNecessaryBtn: "Απόρριψη Όλων",
          savePreferencesBtn: "Αποθήκευση Προτιμήσεων",
          closeIconLabel: "Κλείσιμο",
          serviceCounterLabel: "Υπηρεσία|Υπηρεσίες",
          sections: [
            {
              title: "Οι επιλογές σας για την ιδιωτικότητα",
              description: "Διαχειριστείτε τις προτιμήσεις σας για cookies.",
            },
            {
              title: "Απαραίτητα Cookies",
              description:
                "Αυτά τα cookies είναι απαραίτητα για τη σωστή λειτουργία του ιστότοπου και δεν μπορούν να απενεργοποιηθούν.",
              linkedCategory: "necessary",
            },
            {
              title: "Analytics & Μετρήσεις",
              description:
                "Κατανόηση χρήσης του ιστότοπου από τους επισκέπτες.",
              linkedCategory: "analytics",
            },
            {
              title: "Newsletter και Marketing",
              description:
                "Αυτά τα cookies χρησιμοποιούνται για να κάνουν τα διαφημιστικά μηνύματα πιο σχετικά με εσάς και τα ενδιαφέροντά σας. Στόχος είναι η εμφάνιση διαφημίσεων που είναι σχετικές και ελκυστικές για κάθε χρήστη και επομένως πιο πολύτιμες για τους εκδότες και τους τρίτους διαφημιστές.",
              linkedCategory: "marketing",
            },
            {
              title: "Περισσότερες πληροφορίες",
              description:
                'Για οποιαδήποτε ερώτηση σχετικά με την πολιτική μας για τα cookies και τις επιλογές σας, παρακαλούμε <a href="/privacy-policy">επικοινωνήστε μαζί μας</a>',
            },
          ],
        },
      },
    },
  },
});

// Move ALL your functions here (globally available)
let blockedServices = [];
let cookieConsent = {}; // Will be populated by CookieConsent

// Your existing functions (unchanged)
function loadSentry() {
  if (CookieConsent.hasConsent("functionality.sentry")) {
    if (window.Sentry) return console.log("Sentry: Already loaded");
    const script = document.createElement("script");
    script.src =
      "https://js-de.sentry-cdn.com/3b208bcd006ce709256308f182d0c37c.min.js";
    script.crossOrigin = "anonymous";
    script.onload = function () {
      try {
        Sentry.init({
          /* your config */
        });
        console.log("Sentry: Loaded");
      } catch (e) {
        console.warn("Sentry init error:", e);
      }
    };
    document.head.appendChild(script);
  }
}

function loadGoogleAnalytics() {
  if (CookieConsent.hasConsent("analytics.googleAnalytics")) {
    if (window.gtag || window.dataLayer)
      return console.log("GA: Already loaded");
    // Your existing GA code...
    const script1 = document.createElement("script");
    script1.async = true;
    script1.src = "https://www.googletagmanager.com/gtag/js?id=G-86MQLKEQCZ";
    document.head.appendChild(script1);
    // etc...
  }
}

function loadClarity() {
  if (CookieConsent.hasConsent("analytics.clarity")) {
    // Your existing Clarity code...
  }
}

function loadMailchimp() {
  if (CookieConsent.hasConsent("marketing.mailchimp")) {
    const mcSignup = document.getElementById("mc_embed_signup");
    if (mcSignup) {
      mcSignup.classList.add("show-newsletter");
      mcSignup.style.display = "block";
    }
  }
}

function hideMailchimp() {
  const mcSignup = document.getElementById("mc_embed_signup");
  if (mcSignup) {
    mcSignup.classList.remove("show-newsletter");
    mcSignup.style.display = "none";
  }
}

function loadConsentBasedScripts() {
  blockedServices = [];
  window.blockedServices = blockedServices;

  // Load based on CookieConsent state
  setTimeout(() => loadSentry(), 100);
  setTimeout(() => loadGoogleAnalytics(), 200);
  setTimeout(() => loadClarity(), 300);
  setTimeout(() => loadMailchimp(), 500);

  setTimeout(() => {
    if (blockedServices.length > 0) showBlockedServicesNotification();
  }, 1500);
}

// Keep your other functions: showBlockedServicesNotification, etc.
// Update consent checks to use CookieConsent.hasConsent('category.service')

// Global consent check (replaces your window.hasConsentFor)
window.hasConsentFor = function (servicePath) {
  return CookieConsent.hasConsent(servicePath);
};

// Init Mailchimp CSS
document.addEventListener("DOMContentLoaded", function () {
  var link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = "//cdn-images.mailchimp.com/embedcode/classic-071822.css";
  document.head.appendChild(link);
});
