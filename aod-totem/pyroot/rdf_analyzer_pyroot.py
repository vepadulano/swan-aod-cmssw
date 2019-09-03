from __future__ import print_function
import ROOT

print("## RDFAnalyzer.cc ##")

input_files_vec = ROOT.std.vector("string")()
input_files_list = [
"/eos/user/v/vpadulan/SWAN_projects/totem_karol_data/cmstotem_small_ds/FEBCB07E-7A3C-E911-B10C-D4AE52901D66.root",
"/eos/user/v/vpadulan/SWAN_projects/totem_karol_data/cmstotem_small_ds/FCA19DF8-083C-E911-A2D2-A0369FF882E0.root",
"/eos/user/v/vpadulan/SWAN_projects/totem_karol_data/cmstotem_small_ds/FC01E8C7-113C-E911-8B2E-842B2B6E9A5B.root",
"/eos/user/v/vpadulan/SWAN_projects/totem_karol_data/cmstotem_small_ds/FAF762D0-123C-E911-9D1A-90B11C441C8C.root",
"/eos/user/v/vpadulan/SWAN_projects/totem_karol_data/cmstotem_small_ds/FA4A1FD6-073C-E911-B139-0025901C0610.root",
"/eos/user/v/vpadulan/SWAN_projects/totem_karol_data/cmstotem_small_ds/FA156168-093C-E911-8D29-003048F7CC92.root",
"/eos/user/v/vpadulan/SWAN_projects/totem_karol_data/cmstotem_small_ds/FA09E569-803C-E911-90AC-842B2B6AEC35.root",
"/eos/user/v/vpadulan/SWAN_projects/totem_karol_data/cmstotem_small_ds/F88E98FA-7C3C-E911-9FD8-008CFA110B10.root",
"/eos/user/v/vpadulan/SWAN_projects/totem_karol_data/cmstotem_small_ds/F6DE1B98-093C-E911-BB8A-0CC47AD98B8E.root",
"/eos/user/v/vpadulan/SWAN_projects/totem_karol_data/cmstotem_small_ds/F69F07CE-123C-E911-9182-1866DA7F7AD2.root"
]
for infile in input_files_list:
    input_files_vec.push_back(infile)

d_loaded = ROOT.RDataFrame("Events", input_files_vec)
d_in = d_loaded.Range(1000)

print("Data frame created.")

# ------------------
# BEAMSPOT
# ------------------

print("Processing BeamSpot...")

d_beamspot_processed = d_in.Define("beamspot", "recoBeamSpot_offlineBeamSpot__RECO.obj")                           .Define("xBS", "beamspot.x0()")                           .Define("yBS", "beamspot.y0()")                           .Define("zBS", "beamspot.z0()")                           .Define("bs_point", "math::XYZPoint(xBS, yBS, zBS)")
print(d_beamspot_processed.Count().GetValue())

# ------------------
# TRACKS
# ------------------

print("Processing Tracks...")

def nhits_filter(obj):
    nhits_filter_lambda = """
    using namespace reco;
    using namespace ROOT::VecOps;
    auto nhits_filter = [](Track tr)
    {{
        return tr.hitPattern().numberOfValidPixelHits() > 0;
    }};
    auto tracks_filter = [&nhits_filter](RVec<Track> v)
    {{
        return Filter(v, nhits_filter);
    }};
    return tracks_filter({});
    """.format(obj)
    return nhits_filter_lambda

d_tracks = d_beamspot_processed.Define("all_tracks", "recoTracks_generalTracks__RECO.obj")                               .Filter("! all_tracks.empty()")                               .Define("tracks", nhits_filter("all_tracks"))                               .Filter("! tracks.empty()")
ROOT.gInterpreter.Declare("""
using namespace reco;
using namespace ROOT::VecOps;
""")

d_tracks_processed = d_tracks.Define("hpt",    "return Map(tracks, [](const Track& tr) { return tr.pt(); });").Define("heta",   "return Map(tracks, [](const Track& tr) { return tr.eta(); });").Define("hphi",   "return Map(tracks, [](const Track& tr) { return tr.phi(); });").Define("halgo",  "return Map(tracks, [](const Track& tr) { return tr.algo(); });").Define("hnhits", "return Map(tracks, [](const Track& tr) { return tr.hitPattern().numberOfValidPixelHits(); });").Define("hchi2",  "return Map(tracks, [](const Track& tr) { return tr.normalizedChi2(); });").Define("hd0",    "return Map(tracks, [](const Track& tr) { return tr.d0(); });").Define("hdz",    "return Map(tracks, [](const Track& tr) { return tr.dz(); });").Define("hd0BS",  "return Map(tracks, [&bs_point](const Track& tr) { return tr.dxy(bs_point); });").Define("hdzBS",  "return Map(tracks, [&bs_point](const Track& tr) { return tr.dz(bs_point);  });")
# /* TODO: debug something here in this looper
# .Define("hlooper",[](RVec<Track> v) { return Map(v, [](Track tr){ return tr.isLooper(); }); }, { "tracks" })
# */

nbins_pt = 100
nbins_eta = 80
nbins_phi = 64

h_pt = d_tracks_processed.Histo1D(("hpt", "p_{T}", nbins_pt, 0, 5), "hpt")
h_eta = d_tracks_processed.Histo1D(("heta", "#eta", nbins_eta, -4, 4), "heta")
h_phi = d_tracks_processed.Histo1D(("hphi", "#varphi", nbins_phi, -3.2, 3.2), "hphi")
h_algo = d_tracks_processed.Histo1D(("halgo", "Algo", 15, 0, 15.), "halgo")
h_nhits = d_tracks_processed.Histo1D(("hnhits", "nhits pix+strip", 40, 0, 40.), "hnhits")

h_chi2 = d_tracks_processed.Histo1D(("hchi2", "normalized #chi^{2}", 1050, -50, 1000.), "hchi2")
h_d0 = d_tracks_processed.Histo1D(("hd0", "d0", 2000, -10, 10.), "hd0")
h_dz = d_tracks_processed.Histo1D(("hdz", "dz", 500, -100, 100.), "hdz")

h_d0BS = d_tracks_processed.Histo1D(("hd0BS", "d0", 2000, -10, 10.), "hd0BS")
h_dzBS = d_tracks_processed.Histo1D(("hdzBS", "dz", 500, -100, 100.), "hdzBS")
# /*
# auto h_looper = d_tracks_processed.Histo1D({"hlooper", "isLooper", 5, 0, 5}, "hlooper");
# */

print("Tracks count: {}".format(d_tracks_processed.Count().GetValue()))

# ------------------
# SAVE OUTPUT
# ------------------

fout_name = "out_rdf.root"
print("Saving results to {}".format(fout_name))
fout = ROOT.TFile(fout_name, "RECREATE")
fout.cd()

#  Tracks
h_pt.Write()
h_eta.Write()
h_phi.Write()
h_algo.Write()
h_nhits.Write()

h_chi2.Write()
h_d0.Write()
h_dz.Write()

h_d0BS.Write()
h_dzBS.Write()

# ------------------
# DRAW AN HISTOGRAM
# ------------------

c = ROOT.TCanvas()
h_pt.Draw()
c.SaveAs("h_pt.png")
