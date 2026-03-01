const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const autoprefixer = require("autoprefixer");
const path = require("path");

module.exports = {
  entry: {
    cafe: "./style/screens/cafe/index.scss",
    common: "./style/common.scss",
    collections: "./style/screens/cafe/collections.scss",
    navbar: "./style/components/navbar.scss",
    cafes: "./style/screens/cafe/cafes.scss",
    debug: "./script/debug.js",
    bookCafe: "./style/screens/cafe/book-cafe.scss",
    commonBlog: "./style/commonBlog.scss",
    landing: "./style/landing.scss",
    bio: "./style/bio.scss",
    cookieConsentConfig: "./script/cookieconsent-config.js"
  },
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "dist/style"),
    clean: true,
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].css",
    }),
  ],
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: [autoprefixer],
              },
            },
          },
          {
            loader: "sass-loader",
            options: {
              implementation: require("sass"),
            },
          },
        ],
      },
      {
        test: /\.(woff(2)?|ttf|eot|svg)$/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "[name].[ext]",
              outputPath: "fonts/",
              publicPath: "/fonts/",
            },
          },
        ],
      },
      {
        test: /\.(png|jpe?g|gif|svg|webp|avif)$/,
        type: "asset/resource",
        generator: {
          filename: "images/[name][ext]",
          publicPath: "/images/",
        },
      },
    ],
  },
};