#ifndef LAB1_ARKANOID_GAMEOBJECT_H
#define LAB1_ARKANOID_GAMEOBJECT_H

#include "Point.h"

namespace arkanoid {

    enum class Quadrant {
        I,
        II,
        III,
        IV
    };

    class GameObject
    {
    public:
        GameObject(
                Point topLeft, double maxPositioX, double maxPositionY,
                double width, double height,
                double velocity, double angle);

        virtual ~GameObject() = 0;

        Point topLeft() const;
        void setTopLeft(Point topLeft);
        Point bottomRight() const;

        double velocity() const;
        void setVelocity(double velocity);

        double angle() const;
        void setAngle(double angle);

        double quadrantAngle() const;
        Quadrant quadrant() const;

        double width() const;
        double height() const;

        virtual void move(double elapsedTimeInMS);

        bool reflectIfHit(const GameObject& obj);

    private:
        void reflectFromQuadrantOneIfHit(const GameObject& obj);
        void reflectFromQuadrantTwoIfHit(const GameObject& obj);
        void reflectFromQuadrantThreeIfHit(const GameObject& obj);
        void reflectFromQuadrantFourIfHit(const GameObject& obj);

        void reflectToQuadrantFourIfIntersectsWithX(const GameObject& obj);
        void reflectToQuadrantTwoIfIntersectsWithY(const GameObject& obj);

        void reflectToQuadrantThreeIfIntersectsWithX(const GameObject& obj);
        void reflectToQuadrantOneIfIntersectsWithY(const GameObject& obj);

        void reflectToQuadrantTwoIfIntersectsWithX(const GameObject& obj);
        void reflectToQuadrantFourIfIntersectsWithY(const GameObject& obj);

        void reflectToQuadrantOneIfIntersectsWithX(const GameObject& obj);
        void reflectToQuadrantThreeIfIntersectsWithY(const GameObject& obj);

        void toQuadrantOne();
        void toQuadrantTwo();
        void toQuadrantThree();
        void toQuadrantFour();

        Point mTopLeft;
        const double mMaxPositionX;
        const double mMaxPositionY;

        const double mWidth;
        const double mHeight;

        double mVelocity;
        Quadrant mQuadrant;
        double mQuadrantAngle;
    };

    bool isInQuadrantOne(double angle);
    bool isInQuadrantTwo(double angle);
    bool isInQuadrantThree(double angle);
    bool isInQuadrantFour(double angle);

    bool interectsWithRightX(const GameObject& a, const GameObject& b);
    void putBeforeIntersectsWithRightX(GameObject& a, const GameObject& b);

    bool interectsWithLeftX(const GameObject& a, const GameObject& b);
    void putBeforeIntersectsWithLeftX(GameObject& a, const GameObject& b);

    bool interectsWithBottomY(const GameObject& a, const GameObject& b);
    void putBeforeIntersectsWithBottomY(GameObject& a, const GameObject& b);

    bool interectsWithTopY(const GameObject& a, const GameObject& b);
    void putBeforeIntersectsWithTopY(GameObject& a, const GameObject& b);

    bool isInsideWithY(const GameObject& a, const GameObject& b);
    bool isInsideWithX(const GameObject& a, const GameObject& b);

    bool intersectsFromRigthWithX(const GameObject& a, const GameObject& b);
    bool intersectsFromLeftWithX(const GameObject& a, const GameObject& b);
    bool intersectsFromTopWithY(const GameObject& a, const GameObject& b);
    bool intersectsFromBottomWithY(const GameObject& a, const GameObject& b);

    Point calcDelta(double quadrantAngle, Quadrant quadrant, double sideC);

    double calcTraveldWay(double deltaTimeMS, double velocityInS);

    double calcAlphaIfOver360(double alpha);

    Quadrant calcQuadrant(double alpha);

    double angleToQuadrantAngle(double angle, Quadrant quadrant);

    double qudrantAngleToAngle(double quadrantAngle, Quadrant quadrant);

    double increaseAngle(double quadrantAngle);

    double decreaseAngle(double quadrantAngle);

    double mirror(double quadrantAngle);
}  // namespace arkanoid

#endif //LAB1_ARKANOID_GAMEOBJECT_H
