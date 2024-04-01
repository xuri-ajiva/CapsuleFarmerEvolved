from threading import Thread
from time import sleep
from rich.live import Live
from rich.table import Table
from rich.console import Console

class GuiThread(Thread):
    """
    A thread that creates a capsule farm for a given account
    """

    def __init__(self, log, config, stats, locks):
        """
        Initializes the FarmThread

        :param log: Logger object
        :param config: Config object
        :param stats: Stats, Stats object
        """
        super().__init__()
        self.log = log
        self.config = config
        self.stats = stats
        self.locks = locks
    
    def generateTable(self, header):
        table = Table(show_header=header, show_edge=False)
        table.add_column("Account")
        table.add_column("Status")
        table.add_column("Live matches")
        table.add_column("Heartbeat")
        table.add_column("Last drop")
        table.add_column("Session Drops")
        if self.config.showHistoricalDrops:
            table.add_column("Lifetime Drops")

        for acc in self.stats.accountData:
            status = self.stats.accountData[acc]["status"]
            if self.config.showHistoricalDrops:
                table.add_row(f"{acc}", f"{status}", f"{self.stats.accountData[acc]['liveMatches']}", f"{self.stats.accountData[acc]['lastCheck']}", f"{self.stats.accountData[acc]['lastDrop']}", f"{self.stats.accountData[acc]['sessionDrops']}", f"{self.stats.accountData[acc]['totalDrops']}")
            else:
                table.add_row(f"{acc}", f"{status}", f"{self.stats.accountData[acc]['liveMatches']}", f"{self.stats.accountData[acc]['lastCheck']}", f"{self.stats.accountData[acc]['lastDrop']}", f"{self.stats.accountData[acc]['sessionDrops']}")

        return table

    def run(self):
        """
        Report the status of all accounts
        """
        console = Console(force_terminal=True)
        i = 0;
        while True:
            console.print(self.generateTable((i%100) == 0))
            sleep(10)
            i += 1

    def stop(self):
        """
        Try to stop gracefully
        """
        pass
