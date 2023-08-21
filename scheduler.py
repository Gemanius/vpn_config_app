import schedule

def scheduler(config_service):
    schedule.every(60).minutes.do(config_service.update_configs)

    def running_schedule():
        while True:
            schedule.run_pending()
            
    running_schedule()
    
        