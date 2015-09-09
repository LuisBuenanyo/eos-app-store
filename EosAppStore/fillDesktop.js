//-*- mode: js; js-indent-level: 4; indent-tabs-mode: nil -*-

const AppListModel = imports.appListModel;
const Categories = imports.categories;
const Environment = imports.environment;
const EosAppStorePrivate = imports.gi.EosAppStorePrivate;
const Gio = imports.gi.Gio;
const Lang = imports.lang;

const FILL_DESKTOP_NAME = 'com.endlessm.AppStore.FillDesktop';

const FillDesktop = new Lang.Class({
    Name: 'FillDesktop',
    Extends: Gio.Application,

    _init: function() {
        this._appModel = null;
        this._appList = null;
        this._appInfos = [];

        Environment.loadResources();

        this.parent({ application_id: FILL_DESKTOP_NAME });
    },

    vfunc_startup: function() {
        this.parent();

        this._appModel = new EosAppStorePrivate.AppListModel();
    },

    vfunc_activate: function() {
        this.hold();

        this._appList = new AppListModel.AppList();
        this._appList.refresh(Lang.bind(this, this._onModelRefresh));
    },

    _onModelRefresh: function(error) {
        if (error) {
            logError(error, 'Error while refreshing the model');
            return;
        }

        let categories = Categories.get_app_categories();
        for (let c in categories) {
            let category = categories[c].id;
            // INSTALLED is just a pseudo-category; we'll get all the apps by
            // using the other categories already, and then we'll remove from
            // the list those that are already installed with a launcher later.
            if (category == EosAppStorePrivate.AppCategory.INSTALLED)
                continue;

            this._appInfos = this._appInfos.concat(this._appList.loadCategory(category));
        }

        // Remove apps that are not installed on the device
        // or that already have a launcher
        this._appInfos = this._appInfos.filter(function(app) {
            return !app.get_has_launcher() && app.is_installed();
        });

        this._install();
    },

    _install: function() {
        let app = this._appInfos.pop();
        if (!app) {
            this.release();
            return;
        }

        let appId = app.get_desktop_id();
        this._appList.install(appId, Lang.bind(this, function(error) {
            this._install();
        }));
    },

    get appModel() {
        return this._appModel;
    }
});

function main() {
    Environment.init();

    let app = new FillDesktop();
    return app.run(ARGV);
}
