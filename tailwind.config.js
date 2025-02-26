module.exports = {
  daisyui: {
    themes: [
      {
        mytheme: {
          primary: "#635642",

          secondary: "#2f2e41",

          accent: "#a8dadc",

          neutral: "#333333",

          "base-100": "#f5f5f5",

          info: "#3abff8",

          success: "#36d399",

          warning: "#fbbd23",

          error: "#f87272",
        },
      },
    ],
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
};
