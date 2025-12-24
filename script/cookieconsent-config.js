import * as Sentry from "@sentry/browser";

const APP_TYPE = (() => {
  const hostname = location.hostname;
  if (hostname.includes("cafe.")) return "cafe";
  if (hostname.includes("blog.")) return "blog";
  return "main";
})();

const APP_CONFIGS = {
  blog: {
    gtag_id: "",
    clarity_id: "",
    plausible_domain: "blog.book-community.com",
    sentry_dsn:
      "https://3b208bcd006ce709256308f182d0c37c@o4509735697186816.ingest.de.sentry.io/4509735911227472",
    sentry_environment: "blog",
  },
  cafe: {
    gtag_id: "G-86MQLKEQCZ",
    clarity_id: "sl12n9f03c",
    plausible_domain: "cafe.book-community.com",
    sentry_dsn:
      "https://3b208bcd006ce709256308f182d0c37c@o4509735697186816.ingest.de.sentry.io/4509735911227472",
    sentry_environment: "cafe",
  },
  main: {
    gtag_id: "",
    clarity_id: "",
    plausible_domain: "book-community.com",
    sentry_dsn:
      "https://3b208bcd006ce709256308f182d0c37c@o4509735697186816.ingest.de.sentry.io/4509735911227472",
    sentry_environment: "main",
  },
};

const currentAppConfig = APP_CONFIGS[APP_TYPE] || APP_CONFIGS.main;

const CookieConsentFun = () => {
  CookieConsent.run({
    categories: {
      necessary: { enabled: true, readOnly: true },
      functionality: {
        label: "Λειτουργικότητα",
        description: "Παρακολούθηση σφαλμάτων.",
        cookies: [
          {
            id: "sentry",
            name: "sentry-*",
            domain: ".sentry.io",
            path: "/",
            category: "functionality",
          },
        ],
      },
      analytics: {
        label: "Analytics & Μετρήσεις",
        description: "Ανάλυση επισκεψιμότητας.",
        cookies: [
          ...(currentAppConfig.gtag_id
            ? [
                {
                  id: "google-analytics",
                  name: "_ga,_gid,_gat",
                  domain: ".book-community.com",
                  path: "/",
                  category: "analytics",
                },
              ]
            : []),
          ...(currentAppConfig.clarity_id
            ? [
                {
                  id: "clarity",
                  name: "_clck,_clsk,CLID",
                  domain: ".book-community.com",
                  path: "/",
                  category: "analytics",
                },
              ]
            : []),
        ],
      },
      marketing: {
        label: "Marketing & Newsletter",
        description: "Newsletter.",
        cookies: [
          {
            id: "mailchimp",
            name: "_mcid",
            domain: ".book-community.com",
            path: "/",
            category: "marketing",
          },
        ],
      },
    },
    language: {
      default: "el",
      translations: {
        el: {
          consentModal: {
            title: "🍪 Χρήση Cookies",
            description: "Βελτιώνουμε την εμπειρία σας.",
            acceptAllBtn: "Αποδοχή Όλων",
            acceptNecessaryBtn: "Μόνο Απαραίτητα",
            showPreferencesBtn: "Ρυθμίσεις",
          },
          preferencesModal: {
            title: "Ρυθμίσεις Cookies",
            acceptAllBtn: "Αποδοχή Όλων",
            acceptNecessaryBtn: "Απόρριψη Όλων",
            savePreferencesBtn: "Αποθήκευση",
            sections: [
              {
                title: "Οι επιλογές σας",
                description: "Διαχειριστείτε cookies.",
              },
              {
                title: "Απαραίτητα",
                description: "Απαραίτητα για λειτουργία.",
                linkedCategory: "necessary",
              },
              {
                title: "Analytics",
                description: "Ανάλυση χρήσης.",
                linkedCategory: "analytics",
              },
              {
                title: "Marketing",
                description: "Newsletter.",
                linkedCategory: "marketing",
              },
              {
                title: "Πληροφορίες",
                description:
                  '<a href="https://cafe.book-community.com/page/privacy-policy/">Πολιτική</a>',
              },
            ],
          },
        },
      },
    },
    guiOptions: {
      consentModal: { layout: "cloud", position: "bottom center" },
      preferencesModal: { layout: "box", position: "right panel" },
    },

    onFirstConsent: ({ cookie }) => loadConsentBasedScripts(cookie),
    onConsent: ({ cookie }) => loadConsentBasedScripts(cookie),
  });

  let blockedServices = [];

  function hasConsentFor(cookie, category) {
    const acceptedCategories = cookie?.level || [];
    const isInLoad =
      Array.isArray(acceptedCategories) &&
      acceptedCategories.includes(category);
    return isInLoad ?? false;
  }

  function loadSentry(cookie) {
    if (
      hasConsentFor(cookie, "functionality") &&
      currentAppConfig.sentry_dsn &&
      !window.Sentry
    ) {
      const script = document.createElement("script");
      script.src = currentAppConfig.sentry_dsn.split("@")[0] + ".min.js";
      script.crossOrigin = "anonymous";
      script.onload = () =>
        Sentry.init({
          dsn: "https://3b208bcd006ce709256308f182d0c37c@o4509735697186816.ingest.de.sentry.io/4509735911227472",
          integrations: [Sentry.browserTracingIntegration()],
          tracesSampleRate: 1.0,
          sendDefaultPii: true,
        });
      script.onerror = () => blockedServices.push("Sentry");
      document.head.appendChild(script);
    }
  }

  function loadGoogleAnalytics(cookie) {
    if (
      hasConsentFor(cookie, "analytics") &&
      currentAppConfig.gtag_id &&
      !window.gtag
    ) {
      const script1 = document.createElement("script");
      script1.async = true;
      script1.src = `https://www.googletagmanager.com/gtag/js?id=${currentAppConfig.gtag_id}`;
      script1.onerror = () => blockedServices.push("Google Analytics");
      document.head.appendChild(script1);

      const script2 = document.createElement("script");
      script2.innerHTML = `window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${currentAppConfig.gtag_id}',{anonymize_ip:true});`;
      document.head.appendChild(script2);
    }
  }

  function loadClarity(cookie) {
    if (
      hasConsentFor(cookie, "analytics") &&
      currentAppConfig.clarity_id &&
      !window.clarity
    ) {
      (function (c, l, a, r, i, t, y) {
        c[a] =
          c[a] ||
          function () {
            (c[a].q = c[a].q || []).push(arguments);
          };
        t = l.createElement(r);
        t.async = 1;
        t.src = "https://www.clarity.ms/tag/" + i;
        y = l.getElementsByTagName(r)[0];
        y.parentNode.insertBefore(t, y);
      })(window, document, "clarity", "script", currentAppConfig.clarity_id);
    }
  }

  function loadMailchimp(cookie) {
    if (hasConsentFor(cookie, "marketing")) {
      const mcSignup = document.getElementById("mc_embed_signup");
      if (mcSignup) mcSignup.style.display = "block";
    }
  }

  function loadConsentBasedScripts(cookie) {
    blockedServices = [];

    setTimeout(() => loadSentry(cookie), 100);
    setTimeout(() => loadGoogleAnalytics(cookie), 300);
    setTimeout(() => loadClarity(cookie), 400);
    setTimeout(() => loadMailchimp(cookie), 500);

    // setTimeout(() => {
    //   if (blockedServices.length > 0) showBlockedServicesNotification();
    // }, 1500);
  }

  function showBlockedServicesNotification() {
    if (blockedServices.length === 0) return;

    const notification = document.createElement("div");
    notification.style.cssText =
      "position:fixed;top:20px;right:20px;background:#F8F4E9;color:#635642;padding:15px;border-radius:8px;border:2px solid #8B7355;z-index:10002;font-family:Arial;max-width:350px;";
    notification.innerHTML = `🛡️ Μερικές υπηρεσίες αναλύσεων μπλοκαρίστηκαν (ad blocker).<button onclick="this.parentElement.remove()" style="margin-left:10px;background:none;border:none;font-size:18px;cursor:pointer;">×</button>`;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 8000);
  }

  window.hasConsentFor = (category) =>
    hasConsentFor(CookieConsent.getCookie(), category);
};

const doesUserScroll = () => {
  let scrolled = false;
  window.addEventListener("scroll", () => {
    if (scrolled) return;
    CookieConsentFun();
    scrolled = true;
  });
  return () => scrolled;
};

doesUserScroll();
