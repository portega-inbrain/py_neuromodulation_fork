import mne
import mne_bids
import pybv
import os


def set_chtypes(vhdr_raw):
    """
    define MNE RawArray channel types
    """
    print('Setting new channel types...')
    remapping_dict = {}
    for ch_name in vhdr_raw.info['ch_names']:
        if ch_name.startswith('ECOG'):
            remapping_dict[ch_name] = 'ecog'
        elif ch_name.startswith(('LFP', 'STN')):
            remapping_dict[ch_name] = 'seeg'
        elif ch_name.startswith('EMG'):
            remapping_dict[ch_name] = 'emg'
        elif ch_name.startswith('EEG'):
            remapping_dict[ch_name] = 'misc'
        elif ch_name.startswith(('MOV', 'ANALOG', 'ROT', 'ACC', 'AUX', 'X', 'Y', 'Z')):
            remapping_dict[ch_name] = 'misc'
        else:
            remapping_dict[ch_name] = 'misc'
    vhdr_raw.set_channel_types(remapping_dict, verbose=False)
    return vhdr_raw


if __name__ == "__main__":
    # define run file to read and write from
    PATH_RUN = r"C:\Users\ICN_admin\Documents\Decoding_Toolbox\Data\Berlin_VoluntaryMovement\sub-002\ses-EphysMedOff02\ieeg\sub-002_ses-EphysMedOff02_task-SelfpacedRotationR_acq-StimOff_run-01_ieeg.vhdr"

    entities = mne_bids.get_entities_from_fname(PATH_RUN)
    bids_path = mne_bids.BIDSPath(subject=entities["subject"], session=entities["session"], task=entities["task"],
                                  run=entities["run"], acquisition=entities["acquisition"], datatype="ieeg",
                                  root=r"C:\Users\ICN_admin\Documents\Decoding_Toolbox\Data\Berlin_VoluntaryMovement")
    raw_arr = mne_bids.read_raw_bids(bids_path)

    # crop data
    raw_arr.crop(102, 120)  # pick three movements

    pybv.write_brainvision(data=raw_arr.get_data(), sfreq=raw_arr.info["sfreq"], ch_names=raw_arr.ch_names,
                           fname_base="example", folder_out=os.getcwd())

    data_to_write = mne.io.read_raw_brainvision("example.vhdr")

    # example.eeg / .vhdr need to be deleted afterwards

    data_to_write = set_chtypes(data_to_write)
    data_to_write.info["line_freq"] = 50

    mne_bids.write_raw_bids(data_to_write, mne_bids.BIDSPath(subject="testsub", session="EphysMedOff",
                            task="buttonpress", datatype="ieeg", run="0",
                            root=r"C:\Users\ICN_admin\Documents\py_neuromodulation\examples\data"),
                            overwrite=True)
