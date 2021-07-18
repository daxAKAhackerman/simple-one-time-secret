// vetur.config.js
/** @type {import('vls').VeturConfig} */
module.exports = {
    // **optional** default: `{}`
    // override vscode settings
    // Notice: It only affects the settings used by Vetur.
    settings: {
        "vetur.useWorkspaceDependencies": false,
        "vetur.experimental.templateInterpolationService": false
    },
    // **optional** default: `[{ root: './' }]`
    // support monorepos
    projects: [
        {
            root: './client',
            package: './package.json',
            jsconfig: './jsconfig.json',
            globalComponents: [
                './src/components/**/*.vue'
            ]
        }
    ]
}
