const autoprefixer = require("autoprefixer");

module.exports = {
	mode: "development",
	entry: [
		"./style/theme.scss",
		"./app.js",
		"./style/index.scss",
		"./style/cafes.scss",
		"./style/cafe.scss",
		"./style/article-components.scss",
		"./style/inside-article.scss",
		"./style/page404.scss",
		"./style/footer.scss",
		"./style/landing.scss",
	],
	output: {
		filename: "bundle.js",
	},
	module: {
		rules: [
			{
				test: /\.scss$/,
				use: [
					{
						loader: "file-loader",
						options: {
							name: "[path][name].css",
						},
					},
					{ loader: "extract-loader" },
					{ loader: "css-loader" },
					{
						loader: "postcss-loader",
						options: {
							postcssOptions: {
								plugins: [autoprefixer()],
							},
						},
					},
					{
						loader: "sass-loader",
						options: {
							// Prefer Dart Sass
							implementation: require("sass"),

							// See https://github.com/webpack-contrib/sass-loader/issues/804
							webpackImporter: false,
							sassOptions: {
								includePaths: ["./node_modules"],
							},
						},
					},
				],
			},
		],
	},
};
