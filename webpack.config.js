const ExtractTextPlugin = require("extract-text-webpack-plugin");
const path = require("path");
const webpack = require("webpack");
const isProd = process.env.NODE_ENV === 'development';

const plugins = [
    new ExtractTextPlugin("../styles/client.css"),
];

// Production configs and setup
if (isProd) {
    plugins.push(
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify('production')
            }
        }),
        new webpack.LoaderOptionsPlugin({
            minimize: true,
            debug: false
        }),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false,
                screw_ie8: true,
                conditionals: true,
                unused: true,
                comparisons: true,
                sequences: true,
                dead_code: true,
                evaluate: true,
                if_return: true,
                join_vars: true,
            },
            output: {
                comments: false,
            },
        })
    );
}

module.exports = {
    entry: {
        app:"./src/scripts/controllers/AppController.js",
        main:"./src/scripts/controllers/MainController.js",
    },
    output:{
        path: path.resolve(__dirname, "static/scripts"),
        filename: "[name].min.js",
    },
    module:{
        rules:[
            {
                 test: /\.js$/,
                 exclude:/node_modules/,
                 loader: "babel-loader",
                 query: {
                    presets: ['babel-preset-env'].map(require.resolve),
                 }
            },
            {
                 test: /\.scss$/,
                 use:ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: [
                        {
                            loader: 'css-loader',
                            options: {
                                url: false,
                                minimize: (isProd)? true :false,
                                sourceMap: true
                            }
                        },
                        {
                            loader: 'sass-loader',
                            options: {
                                sourceMap: true
                            }
                        }
                    ],
                    publicPath: '/'
                 })
            }
        ]
    },
    plugins,
    devServer:{
        contentBase: path.join(__dirname, "public"),
        compress:true,
        open:true,
        openPage:"",
        stats:"errors-only"
    }
}

