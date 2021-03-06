//-*- mode: js; js-indent-level: 4; indent-tabs-mode: nil -*-
const Gio = imports.gi.Gio;
const GLib = imports.gi.GLib;
const Gtk = imports.gi.Gtk;

const Lang = imports.lang;

const _PREFIX = 'eos-folder';

const FolderModel = new Lang.Class({
    Name: 'FolderModel',

    getIconList: function() {
        return Gtk.IconTheme.get_default()
            .list_icons(null)
            .filter(function(iconName) {
                return iconName.startsWith(_PREFIX) &&
                    iconName.endsWith('-symbolic');
            });
    },

    createFolder: function(name, iconName) {
        let keyFile = new GLib.KeyFile();

        keyFile.set_value(GLib.KEY_FILE_DESKTOP_GROUP,
                          GLib.KEY_FILE_DESKTOP_KEY_NAME, name);

        keyFile.set_value(GLib.KEY_FILE_DESKTOP_GROUP,
                          GLib.KEY_FILE_DESKTOP_KEY_ICON, iconName);

        keyFile.set_value(GLib.KEY_FILE_DESKTOP_GROUP,
                          GLib.KEY_FILE_DESKTOP_KEY_TYPE, GLib.KEY_FILE_DESKTOP_TYPE_DIRECTORY);

        let dirpath = GLib.build_filenamev([GLib.get_user_data_dir(), '/desktop-directories']);

        // octal literals are deprecated in JS, so use parseInt
        if (GLib.mkdir_with_parents(dirpath, parseInt('0755', 8), null) < 0) {
            log('could not create the directory ' + dirpath);
            return;
        }

        let dir =  Gio.File.new_for_path(dirpath);

        let enumerator = dir.enumerate_children('standard::name',
                                                Gio.FileQueryInfoFlags.NONE, null);

        let prefix = 'eos-folder-user-';
        let suffix = '.directory';
        let re = new RegExp(prefix + '([0-9]+)' + suffix);
        let n = -1;

        for (let f = enumerator.next_file(null); f != null; f = enumerator.next_file(null)) {
            let result = re.exec(f.get_name());
            if (result != null) {
                let new_n = result[1];
                n = Math.max(n, parseInt(new_n));
            }
        }
        enumerator.close(null);

        let filename = prefix + (n+1) + suffix;

        let buf = keyFile.to_data();

        let channel = GLib.IOChannel.new_file(dirpath + '/' + filename, 'w');
        channel.write_chars(buf[0], buf[1]);
        channel.shutdown(true);

        let application = Gio.Application.get_default();
        let shellProxy = application.shellProxy;
        shellProxy.proxy.AddFolderRemote(filename);
    }
});
