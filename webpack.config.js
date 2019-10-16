const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin').CleanWebpackPlugin

// to minify the js files
//const TerserPlugin = require('terser-webpack-plugin')
// to create a main css style file
//const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
	entry: {
		main: "./MR_Blog/public/assets/app.js",
		dashboard: "./MR_Blog/public/assets/dashboard.js"
	},
	output: {
		filename: "[name]-bundle.js",
		path: path.resolve("./MR_Blog/public/static/dist"),
		publicPath: "./MR_Blog/public/static/dist/"
	},
	mode: 'development',
	module: {
		rules: [
			{
				test: /\.(jpg|png)$/,
				use: "file-loader"
			},
			{
				test: /\.css$/,
				use: [MiniCssExtractPlugin.loader, 'css-loader']
			},
			{
				test: /\.js$/,
				exclude: /node_modules/,
				use: {
					loader: 'babel-loader',
					options: {
						presets: ['@babel/env'],
						plugins: ['transform-class-properties']
					}
				}
			},
			{
				test: /.(ttf|otf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/,
				use: [{
					loader: 'file-loader',
					options: {
						name: '[name].[ext]',
						outputPath: 'fonts/',
						publicPath: 'fonts/'
					}
				}]
			}
		]
	},
	plugins: [
		new MiniCssExtractPlugin({
			filename: '[name].css'
		}),
		new CleanWebpackPlugin(),
		//new TerserPlugin(),
		//new HtmlWebpackPlugin()
	]
}