package logger

import (
	"os"

	"github.com/sirupsen/logrus"
)

// New creates a configured Logrus logger instance.
func New(serviceName string) *logrus.Logger {
	log := logrus.New()
	log.SetFormatter(&logrus.TextFormatter{
		FullTimestamp:   true,
		TimestampFormat: "2006-01-02 15:04:05",
	})
	log.SetOutput(os.Stdout)
	log.SetLevel(logrus.InfoLevel)
	log.WithField("service", serviceName)
	return log
}
