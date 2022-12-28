class SoftDeletes:

    def active(self):
        return self.filter(date_deleted=None)

    def trashed(self):
        return self.exclude(date_deleted=None)
