from dna_features_viewer import BiopythonTranslator

graphic_record = BiopythonTranslator().translate_record("example_sequence.gb")
ax, _ = graphic_record.plot(figure_width=10, strand_in_label_threshold=7)
ax.figure.tight_layout()
ax.figure.savefig("from_genbank.png")
