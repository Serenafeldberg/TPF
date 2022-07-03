from notes import frecuency

class Note ():
    def __init__ (self, file):
        self.file = file
        self.frecuency = frecuency

    def read_file (self):
        self.notes = {}
        with open(self.file, 'r') as fn:
            lines = fn.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip('\n')
                line = lines[i].split()
                frec = self.frecuency[line[1]]
                self.notes[i] = [float(line[0]), frec, float(line[2])]

        return self.notes

    def get_duration (self):
        '''
        Returns the total duration of the song (partiture)
        '''
        duration = 0
        bucket = 0
        notes = self.read_file()
        notes_in_order = sorted(notes.values())

        if notes_in_order[0][0] != 0:
            duration += notes_in_order[0][0]

        for value in notes_in_order:
            tstart = value[0]
            d_note = value[2]
            tend = tstart + d_note
            if tend > bucket:
                if tstart < bucket:
                    d_note = tend - bucket

                if tstart > bucket:
                    blank_secs = tstart - bucket
                    duration += blank_secs
                    bucket += blank_secs

                bucket = tend
                duration += d_note
                
        return duration



